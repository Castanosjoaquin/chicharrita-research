"""La regla de conteo del si-Fi21 original: un registro por acierto de Bowtie.

Por que existe. La columna «Efficient siRNA hits» del si-Fi21 original **no cuenta
ventanas**: cuenta aciertos de Bowtie. En `general_helpers.py:107-123`,
`get_table_data` arma la tabla con
`Counter(player['hit_name'] for player in query if player['is_efficient'])`, o sea
un registro por acierto, agrupado por el nombre de la referencia contra la que
pego `[R]`. Y en `sifi_pipeline.py:195-221` hay dos caminos para construir el
registro: si hay acierto, `hit_name` es el nombre de la referencia; si no lo hay,
`hit_name = False` y `strand = None`, y como todo el bloque de eficiencia vive
dentro de `if strand == '+'`, esa ventana **nunca se evalua** `[R]`.

De ahi salen tres consecuencias que ningun barrido de parametros podia capturar:
una ventana eficiente que no pega en la referencia elegida no entra al conteo; una
que pega solo en la hebra menos tampoco entra; y una que pega dos veces en la misma
referencia cuenta dos veces. Este script implementa esa regla y la mide.

Que hace, y que NO hace:
  - Lee el TSV por ventana del port (`tools/sifi21_port/run_sifi.py --salida`), del
    que solo usa `pos`, `seq` e `is_efficient`.
  - Lee los aciertos de una salida de Bowtie (`-a -v 0`, o `-v 1` como
    sensibilidad), en formato nativo o SAM; o los enumera localmente contra un
    FASTA por coincidencia exacta, que es lo mismo que `-a -v 0` reporta.
  - Devuelve, por gen y por base: (a) el conteo por ventana, (b) el conteo por
    acierto en la hebra mas, (c) el conteo por acierto en cualquier hebra,
    (d) cuantas ventanas eficientes no pegan y (e) cuantas pegan mas de una vez.
    Y la tabla desagregada por referencia, que es la unidad en la que el original
    presenta sus filas.
  - Compara cada celda contra un vector declarado, con tres agregaciones
    explicitas (suma de filas, fila mayor, fila homonima del gen), porque no
    sabemos que fila de la tabla leyo el laboratorio.
  - NO reimplementa el criterio de eficiencia: eso lo calcula el port y entra por
    el TSV. NO corre Bowtie ni RNAplfold.

Confidencialidad: el TSV del port y el FASTA de ventanas que escribe el subcomando
`ventanas` contienen secuencias de EPILAB. Van a `work/`, nunca a `research/`, y no
se suben a ningun servicio web (CLAUDE.md).

Uso:
    # 1. escribir el FASTA de ventanas para alimentar a Bowtie
    python conteo_por_acierto.py ventanas --tsv work/C2/runs/port_fiel/BicC_Dm.tsv \
        --salida work/M1/ventanas/BicC_Dm.fasta

    # 2. correr Bowtie aparte (maquina con bowtie 1.3.1):
    #    bowtie -a -v 0 -f <indice> work/M1/ventanas/BicC_Dm.fasta > hits.txt

    # 3. contar con la regla del original
    python conteo_por_acierto.py contar \
        --gen BicC_Dm=work/C2/runs/port_fiel/BicC_Dm.tsv \
        --aciertos epilab4:BicC_Dm=work/M1/hits/epilab4_BicC_Dm.txt \
        --json resultados/conteo.json --md resultados/matriz.md

    # variante sin Bowtie: enumeracion local exacta contra un FASTA
    python conteo_por_acierto.py contar \
        --gen BicC_Dm=work/C2/runs/port_fiel/BicC_Dm.tsv \
        --base epilab4=work/C2/runs/epilab_full.fasta

    # control de orientacion: el complemento reverso del gen
    python conteo_por_acierto.py revcomp --fasta work/sifi_check/BicC_Dm_full.fasta \
        --salida work/M1/revcomp/BicC_Dm_full.fasta

    # verificaciones
    python test_conteo_por_acierto.py
"""

from __future__ import annotations

import argparse
import csv
import gzip
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

VENTANA = 21

# Los cuatro conteos de la planilla de EPILAB, en el orden en que los reporta.
# Fuente: research/ola2/W5_secuencias_epilab/, repetido en docs/plan_ola4/PLAN_OLA4.md.
DECLARADO = {"MP_MRFV": 114, "CP_MRFV": 35, "BicC_Dm": 199, "ATPaseD_Dm": 33}
ORDEN_GENES = ["MP_MRFV", "CP_MRFV", "BicC_Dm", "ATPaseD_Dm"]

COMPLEMENTO = str.maketrans("ACGTNacgtn", "TGCANtgcan")
# Alfabeto admitido en las ventanas. Los codigos IUPAC ambiguos (R, Y, S, W, K, M,
# B, D, H, V) no se complementan bien con la tabla de arriba y nunca aparecieron en
# el corpus --los cuatro genes de EPILAB son ACGT en mayusculas, verificado en W5--,
# asi que se rechazan en vez de traducirse mal en silencio.
ALFABETO = set("ACGTN")

AGREGACIONES = ("suma_filas", "fila_max", "fila_homonima")

NOMBRE_VENTANA = re.compile(r"^w(\d+)$")


# --- Tipos ------------------------------------------------------------------

@dataclass(frozen=True, order=True)
class Acierto:
    """Un alineamiento de Bowtie: una ventana contra una posicion de una referencia.

    `pos` es la posicion de inicio de la ventana sobre la consulta, 1-based, la
    misma que trae el TSV del port. `offset` es 0-based sobre la referencia, como
    lo reporta Bowtie. La tupla completa identifica el alineamiento, asi que dos
    aciertos de la misma ventana en la misma referencia y distinto offset son dos
    registros distintos, que es exactamente lo que infla una fila de la tabla.
    """
    pos: int
    ref: str
    hebra: str
    offset: int


# --- Lectura ----------------------------------------------------------------

def abrir(ruta: Path):
    """Abre texto plano o gzip segun la extension."""
    ruta = Path(ruta)
    if ruta.suffix == ".gz":
        return gzip.open(ruta, "rt", encoding="utf-8", errors="replace")
    return open(ruta, "r", encoding="utf-8", errors="replace")


def leer_ventanas(ruta: Path) -> dict[int, dict]:
    """pos -> {'seq': str, 'eficiente': bool} desde el TSV del port.

    Del TSV solo se usan tres columnas. El resto de los terminos del veredicto se
    ignora a proposito: la eficiencia ya esta decidida y aca no se recalcula.
    """
    out: dict[int, dict] = {}
    with abrir(ruta) as fh:
        for fila in csv.DictReader(fh, delimiter="\t"):
            if "pos" not in fila or "is_efficient" not in fila:
                raise SystemExit(f"{ruta}: falta la columna pos o is_efficient")
            pos = int(fila["pos"])
            if pos in out:
                raise SystemExit(f"{ruta}: la posicion {pos} aparece dos veces")
            out[pos] = {
                "seq": (fila.get("seq") or "").strip().upper(),
                "eficiente": str(fila["is_efficient"]).strip().lower() == "true",
            }
    if not out:
        raise SystemExit(f"{ruta}: TSV vacio")
    return out


def leer_fasta(ruta: Path) -> list[tuple[str, str]]:
    """[(nombre, secuencia)]. El nombre es el primer token, como hace Bowtie."""
    nombre, buf, out = None, [], []
    with abrir(ruta) as fh:
        for linea in fh:
            linea = linea.strip()
            if linea.startswith(">"):
                if nombre is not None:
                    out.append((nombre, "".join(buf)))
                partes = linea[1:].strip().split()
                nombre, buf = (partes[0] if partes else ""), []
            elif linea:
                buf.append(linea)
    if nombre is not None:
        out.append((nombre, "".join(buf)))
    return out


def pos_desde_nombre(nombre: str) -> int:
    """Posicion de la ventana a partir del nombre de la lectura.

    La convencion es `w<pos>`, que es la que escribe el subcomando `ventanas`. Se
    acepta tambien un nombre con **un solo** grupo de digitos, para tolerar un FASTA
    de ventanas armado por otro medio. Lo que no se acepta es un nombre con dos o
    mas grupos de digitos: tomar el ultimo, como hacia la primera version de esta
    funcion, le asigna el acierto a la ventana equivocada sin dar error (`w12_2`
    terminaba en la ventana 2).
    """
    m = NOMBRE_VENTANA.match(nombre)
    if m:
        return int(m.group(1))
    nums = re.findall(r"\d+", nombre)
    if len(nums) == 1:
        return int(nums[0])
    if not nums:
        raise SystemExit(f"nombre de lectura sin posicion: {nombre!r}")
    raise SystemExit(
        f"nombre de lectura ambiguo: {nombre!r} tiene {len(nums)} grupos de digitos; "
        "usa la convencion w<pos> del subcomando `ventanas`")


def parsear_bowtie(ruta: Path) -> list[Acierto]:
    """Aciertos desde una salida de Bowtie, en formato nativo o SAM.

    El formato se detecta por linea y no por archivo: el nativo trae la hebra como
    `+`/`-` en la segunda columna, y SAM trae ahi la bandera, que es un entero. Las
    lecturas no alineadas de SAM (bandera 4) y las cabeceras `@` se descartan.
    """
    out: list[Acierto] = []
    with abrir(ruta) as fh:
        for n, linea in enumerate(fh, 1):
            linea = linea.rstrip("\n")
            if not linea or linea.startswith("@"):
                continue
            c = linea.split("\t")
            if len(c) < 4:
                raise SystemExit(f"{ruta}:{n}: menos de 4 columnas")
            if c[1] in ("+", "-"):
                out.append(Acierto(pos_desde_nombre(c[0]), c[2], c[1], int(c[3])))
            elif c[1].isdigit():
                bandera = int(c[1])
                if bandera & 4:
                    continue
                hebra = "-" if bandera & 16 else "+"
                # SAM es 1-based; Bowtie nativo, 0-based. Se normaliza a 0-based.
                out.append(Acierto(pos_desde_nombre(c[0]), c[2], hebra, int(c[3]) - 1))
            else:
                raise SystemExit(f"{ruta}:{n}: segunda columna {c[1]!r} no es hebra ni bandera")
    return out


# --- Enumeracion local de aciertos -----------------------------------------

def revcomp(seq: str) -> str:
    return seq.translate(COMPLEMENTO)[::-1]


def aciertos_locales(ventanas: dict[int, dict], base: Path, mm: int = 0) -> list[Acierto]:
    """Enumera los aciertos de cada ventana contra un FASTA, sin Bowtie.

    Con `mm=0` esto es exactamente lo que reporta `bowtie -a -v 0`: todas las
    coincidencias perfectas de extremo a extremo, en las dos hebras. Se indexa la
    **consulta** y se recorre la referencia una sola vez, que es la unica forma
    razonable cuando la referencia es un genoma y la consulta son unos miles de
    ventanas (el mismo criterio de `tools/sifi21_port/offtarget_21nt.py`).

    Con `mm=1` equivale a `bowtie -a -v 1`: se usa el palomar sobre dos mitades de
    la ventana --un alineamiento con a lo sumo un desajuste tiene al menos una
    mitad exacta-- y cada candidato se verifica contando desajustes. Es correcto
    pero mucho mas lento: sirve para bases chicas, no para un genoma.

    Tres restricciones declaradas, que es donde la equivalencia con Bowtie se
    apoya en un supuesto y no en una identidad:

      - **Alfabeto.** Solo ACGTN; un codigo IUPAC ambiguo aborta en vez de
        complementarse mal en silencio.
      - **N.** Ni una ventana con N ni un tramo de la referencia con N entran a la
        comparacion, porque una N no aparea y no puede haber alineamiento perfecto.
        Con `mm=1` esto es un poco mas estricto que Bowtie, que por `--nceil`
        tolera algunas N en la lectura y podria gastar su unico desajuste en una
        `[?]`.
      - **Palindromos.** Una ventana igual a su complemento reverso se indexa solo
        en `+`: el alineamiento es el mismo y emitirlo en las dos hebras duplicaria
        el registro. Con ventanas de 21 nt el caso no existe.
    """
    if mm not in (0, 1):
        raise SystemExit("--mm admite 0 o 1")

    vacias = sorted(p for p, d in ventanas.items() if not d["seq"])
    if len(vacias) == len(ventanas):
        raise SystemExit("el TSV no trae la columna seq: la enumeracion local la necesita")
    if vacias:
        raise SystemExit(
            f"{len(vacias)} ventanas sin secuencia (la primera, en la posicion "
            f"{vacias[0]}): la enumeracion local no puede saltearlas sin falsear (d)")
    largos = {len(d["seq"]) for d in ventanas.values()}
    if len(largos) > 1:
        raise SystemExit(f"ventanas de largo heterogeneo: {sorted(largos)}")
    k = largos.pop()
    raros = sorted({c for d in ventanas.values() for c in d["seq"]} - ALFABETO)
    if raros:
        raise SystemExit(f"caracteres fuera de ACGTN en las ventanas: {raros}")

    # Las ventanas con N quedan **fuera del indice**, y es lo correcto: una N no
    # aparea con nada, asi que Bowtie no puede dar un alineamiento de extremo a
    # extremo sin desajustes sobre ella. Esas ventanas caen en (d), que es lo que
    # tambien les pasaria con Bowtie.
    con_n = {p for p, d in ventanas.items() if "N" in d["seq"]}
    if con_n:
        print(f"aviso: {len(con_n)} ventanas contienen N y quedan sin acierto "
              f"(la primera, en la posicion {min(con_n)})", file=sys.stderr)

    # Por hebra: la secuencia que hay que ver en la referencia para que Bowtie
    # reporte esa hebra. En `+` es la ventana; en `-`, su complemento reverso. Una
    # ventana igual a su propio complemento reverso se indexa solo en `+`, para no
    # emitir dos registros del mismo alineamiento; con k impar --21, el caso real--
    # eso no puede pasar, porque la base del medio tendria que ser su complemento.
    buscadas: dict[str, dict[str, list[int]]] = {"+": defaultdict(list), "-": defaultdict(list)}
    for pos, d in ventanas.items():
        if pos in con_n:
            continue
        buscadas["+"][d["seq"]].append(pos)
        if revcomp(d["seq"]) != d["seq"]:
            buscadas["-"][revcomp(d["seq"])].append(pos)

    corte = k // 2
    semillas: dict[str, dict[tuple[int, str], list[int]]] = {}
    if mm == 1:
        for hebra, tabla in buscadas.items():
            idx: dict[tuple[int, str], list[int]] = defaultdict(list)
            for seq, posiciones in tabla.items():
                idx[(0, seq[:corte])].extend(posiciones)
                idx[(1, seq[corte:])].extend(posiciones)
            semillas[hebra] = idx

    out: list[Acierto] = []
    for ref, seq_ref in leer_fasta(base):
        seq_ref = seq_ref.upper()
        for i in range(len(seq_ref) - k + 1):
            trozo = seq_ref[i:i + k]
            # Un tramo de la referencia con N no puede dar un alineamiento perfecto,
            # igual que del lado de la consulta. Las regiones de N de un genoma son
            # grandes, asi que esto ademas ahorra trabajo.
            if "N" in trozo:
                continue
            for hebra in ("+", "-"):
                if mm == 0:
                    for pos in buscadas[hebra].get(trozo, ()):
                        out.append(Acierto(pos, ref, hebra, i))
                else:
                    idx = semillas[hebra]
                    candidatos = set(idx.get((0, trozo[:corte]), ()))
                    candidatos.update(idx.get((1, trozo[corte:]), ()))
                    for pos in candidatos:
                        patron = (ventanas[pos]["seq"] if hebra == "+"
                                  else revcomp(ventanas[pos]["seq"]))
                        if sum(a != b for a, b in zip(patron, trozo)) <= mm:
                            out.append(Acierto(pos, ref, hebra, i))
    return out


# --- La regla ---------------------------------------------------------------

def regla_original(ventanas: dict[int, dict], aciertos: list[Acierto]) -> dict:
    """Aplica la regla de conteo del original y devuelve los cinco numeros y las filas.

    La regla, literal: un registro por acierto en la hebra `+` de una ventana
    eficiente, agrupado por el nombre de la referencia. Una ventana sin acierto no
    se evalua; una que pega solo en `-` tampoco; una que pega dos veces cuenta dos
    veces.

    Los aciertos se deduplican por la tupla completa antes de contar: Bowtie no
    emite dos veces el mismo alineamiento, asi que una linea repetida es ruido del
    archivo y no multiplicidad real.
    """
    aciertos = sorted(set(aciertos), key=lambda a: (a.pos, a.ref, a.hebra, a.offset))
    eficientes = {p for p, d in ventanas.items() if d["eficiente"]}

    filas_mas: Counter[str] = Counter()
    filas_cualquiera: Counter[str] = Counter()
    con_acierto: set[int] = set()
    con_acierto_mas: set[int] = set()
    por_ref_mas: dict[int, Counter[str]] = defaultdict(Counter)
    huerfanos = 0

    for a in aciertos:
        if a.pos not in ventanas:
            huerfanos += 1
            continue
        con_acierto.add(a.pos)
        if a.hebra == "+":
            con_acierto_mas.add(a.pos)
            por_ref_mas[a.pos][a.ref] += 1
        if a.pos in eficientes:
            filas_cualquiera[a.ref] += 1
            if a.hebra == "+":
                filas_mas[a.ref] += 1

    suma_filas = sum(filas_mas.values())
    fila_max = max(filas_mas.items(), key=lambda kv: (kv[1], kv[0])) if filas_mas else (None, 0)
    multiple_en_ref = sum(
        1 for p in eficientes if por_ref_mas[p] and max(por_ref_mas[p].values()) > 1)
    multiple_total = sum(1 for p in eficientes if sum(por_ref_mas[p].values()) > 1)

    return {
        "ventanas_total": len(ventanas),
        # (a) el conteo por ventana: no depende de la base
        "eficientes_por_ventana": len(eficientes),
        # (b) el conteo por acierto en `+`, que es la regla del original
        "aciertos_mas_total": suma_filas,
        # (c) el conteo por acierto en cualquier hebra
        "aciertos_cualquier_hebra_total": sum(filas_cualquiera.values()),
        # (d) ventanas eficientes que no pegan
        "eficientes_sin_acierto": len(eficientes - con_acierto),
        "eficientes_sin_acierto_mas": len(eficientes - con_acierto_mas),
        # (e) ventanas eficientes que pegan mas de una vez
        "eficientes_con_acierto_multiple_en_una_ref": multiple_en_ref,
        "eficientes_con_mas_de_un_acierto_mas": multiple_total,
        "filas": dict(sorted(filas_mas.items(), key=lambda kv: (-kv[1], kv[0]))),
        "filas_cualquier_hebra": dict(
            sorted(filas_cualquiera.items(), key=lambda kv: (-kv[1], kv[0]))),
        "fila_max": {"ref": fila_max[0], "conteo": fila_max[1]},
        "referencias_con_fila": len(filas_mas),
        "aciertos_totales": len(aciertos),
        "aciertos_sin_ventana_en_el_tsv": huerfanos,
    }


def agregar(celda: dict, gen: str, agregacion: str) -> int | None:
    """El numero que iria en la tabla, segun que fila se suponga que leyo el laboratorio.

    No sabemos cual fila tomaron, asi que las tres agregaciones se reportan en
    paralelo y ninguna se declara la verdadera. `fila_homonima` es **la unica** fila
    cuyo nombre de referencia contiene el nombre del gen, que es el caso de la base
    armada con los cuatro genes de EPILAB; si hay dos o mas, la agregacion no es una
    fila sino una suma, asi que devuelve `None` en vez de un numero que parece una
    fila y no lo es. Los nombres que coincidieron quedan en la celda, bajo
    `filas_que_nombran_al_gen`, para poder mirarlos.
    """
    if agregacion == "suma_filas":
        return celda["aciertos_mas_total"]
    if agregacion == "fila_max":
        return celda["fila_max"]["conteo"]
    if agregacion == "fila_homonima":
        candidatos = {ref: v for ref, v in celda["filas"].items() if gen in ref}
        celda["filas_que_nombran_al_gen"] = candidatos
        return next(iter(candidatos.values())) if len(candidatos) == 1 else None
    raise SystemExit(f"agregacion desconocida: {agregacion}")


def distancia(vector: dict[str, int | None], declarado: dict[str, int]) -> int | None:
    """Distancia L1 al vector declarado. None si falta algun gen o no hay declarado."""
    if not declarado:
        return None
    total = 0
    for gen, esperado in declarado.items():
        v = vector.get(gen)
        if v is None:
            return None
        total += abs(v - esperado)
    return total


# --- Subcomandos ------------------------------------------------------------

def pares(valores, sep="=") -> list[tuple[str, str]]:
    out = []
    for v in valores or ():
        if sep not in v:
            raise SystemExit(f"se esperaba NOMBRE{sep}RUTA y vino {v!r}")
        nombre, ruta = v.split(sep, 1)
        out.append((nombre, ruta))
    return out


def cmd_ventanas(a) -> int:
    """Escribe el FASTA de ventanas que alimenta a Bowtie, con el nombre `w<pos>`."""
    ventanas = leer_ventanas(Path(a.tsv))
    salida = Path(a.salida)
    salida.parent.mkdir(parents=True, exist_ok=True)
    faltan = [p for p, d in ventanas.items() if not d["seq"]]
    if faltan:
        raise SystemExit(f"{a.tsv}: {len(faltan)} ventanas sin secuencia")
    with open(salida, "w", encoding="utf-8", newline="\n") as fh:
        for pos in sorted(ventanas):
            fh.write(f">w{pos}\n{ventanas[pos]['seq']}\n")
    print(f"{len(ventanas)} ventanas -> {salida}")
    return 0


def cmd_revcomp(a) -> int:
    """Complemento reverso de un FASTA, para el control de orientacion."""
    registros = leer_fasta(Path(a.fasta))
    salida = Path(a.salida)
    salida.parent.mkdir(parents=True, exist_ok=True)
    with open(salida, "w", encoding="utf-8", newline="\n") as fh:
        for nombre, seq in registros:
            fh.write(f">{nombre}_revcomp\n{revcomp(seq.upper())}\n")
    print(f"{len(registros)} registros -> {salida}")
    return 0


def cmd_contar(a) -> int:
    genes = {n: Path(r) for n, r in pares(a.gen)}
    bases = {n: Path(r) for n, r in pares(a.base)}
    if not genes:
        raise SystemExit("hace falta al menos un --gen NOMBRE=TSV")

    ventanas = {gen: leer_ventanas(ruta) for gen, ruta in genes.items()}

    # --aciertos BASE:GEN=RUTA, con los aciertos ya calculados por Bowtie.
    precalculados: dict[tuple[str, str], Path] = {}
    for clave, ruta in pares(a.aciertos):
        if ":" not in clave:
            raise SystemExit(f"se esperaba BASE:GEN=RUTA y vino {clave}={ruta}")
        base, gen = clave.split(":", 1)
        if gen not in genes:
            raise SystemExit(f"--aciertos nombra el gen {gen!r}, que no esta en --gen")
        precalculados[(base, gen)] = Path(ruta)

    declarado = dict(DECLARADO)
    for gen, valor in pares(a.declarado):
        declarado[gen] = int(valor)
    declarado = {g: v for g, v in declarado.items() if g in genes}

    celdas: dict[str, dict[str, dict]] = defaultdict(dict)
    for (base, gen), ruta in sorted(precalculados.items()):
        celdas[base][gen] = regla_original(ventanas[gen], parsear_bowtie(ruta))
        celdas[base][gen]["origen"] = f"bowtie:{ruta.name}"
    for base, ruta in bases.items():
        for gen in genes:
            if gen in celdas[base]:
                continue  # los aciertos de Bowtie ganan sobre la enumeracion local
            aciertos = aciertos_locales(ventanas[gen], ruta, mm=a.mm)
            celdas[base][gen] = regla_original(ventanas[gen], aciertos)
            celdas[base][gen]["origen"] = f"local:mm{a.mm}:{ruta.name}"

    if not celdas:
        raise SystemExit("no hay ninguna celda: pasa --base o --aciertos")

    # Invariante de la celda de verificacion: contra el gen mismo, toda ventana
    # eficiente tiene que pegar al menos una vez en `+`. El exceso de (b) sobre (a)
    # es, exactamente, la cantidad de aciertos de mas sobre ventanas eficientes.
    problemas = []
    if a.exigir_identidad:
        base = a.exigir_identidad
        if base not in celdas:
            raise SystemExit(f"--exigir-identidad {base}: esa base no se corrio")
        for gen, celda in sorted(celdas[base].items()):
            if celda["eficientes_sin_acierto_mas"]:
                problemas.append(
                    f"{base}/{gen}: {celda['eficientes_sin_acierto_mas']} ventanas "
                    f"eficientes sin acierto en `+` contra la base {base!r}")

    resumen = {
        "declarado": declarado,
        "agregaciones": {},
        "celdas": {base: dict(sorted(g.items())) for base, g in sorted(celdas.items())},
    }
    for agregacion in AGREGACIONES:
        filas = {}
        for base, por_gen in sorted(celdas.items()):
            vector = {gen: agregar(celda, gen, agregacion) for gen, celda in por_gen.items()}
            # `reproduce` mira solo los genes que tienen numero declarado: con un gen
            # de mas sin declarar, comparar los diccionarios enteros daria siempre no.
            filas[base] = {
                "vector": vector,
                "distancia_L1": distancia(vector, declarado),
                "reproduce": bool(declarado) and all(
                    vector.get(g) == v for g, v in declarado.items()),
            }
        resumen["agregaciones"][agregacion] = filas

    genes_tabla = [g for g in ORDEN_GENES if g in genes] + sorted(set(genes) - set(ORDEN_GENES))
    md = render_md(resumen, genes_tabla)
    print(md)
    if problemas:
        print("\n".join(f"FALLA: {p}" for p in problemas), file=sys.stderr)

    if a.json:
        Path(a.json).parent.mkdir(parents=True, exist_ok=True)
        Path(a.json).write_text(json.dumps(resumen, indent=2, ensure_ascii=True) + "\n",
                                encoding="utf-8")
    if a.md:
        Path(a.md).parent.mkdir(parents=True, exist_ok=True)
        Path(a.md).write_text(md + "\n", encoding="utf-8")
    return 1 if problemas else 0


def render_md(resumen: dict, genes: list[str]) -> str:
    """Las tablas: una por agregacion, mas el detalle por celda."""
    lin = []
    declarado = resumen["declarado"]
    lin.append("## Conteos por base, con la regla del original")
    lin.append("")
    lin.append("Declarado por la planilla: " +
               ", ".join(f"{g} = {declarado[g]}" for g in genes if g in declarado) + ".")
    for agregacion, filas in resumen["agregaciones"].items():
        lin.append("")
        lin.append(f"### Agregacion `{agregacion}`")
        lin.append("")
        lin.append("| Base | " + " | ".join(genes) + " | Distancia L1 | Reproduce |")
        lin.append("|" + "---|" * (len(genes) + 3))
        for base, dato in filas.items():
            v = dato["vector"]
            celdas = " | ".join("-" if v.get(g) is None else str(v[g]) for g in genes)
            d = "-" if dato["distancia_L1"] is None else str(dato["distancia_L1"])
            lin.append(f"| `{base}` | {celdas} | {d} | {'si' if dato['reproduce'] else 'no'} |")
    lin.append("")
    lin.append("### Detalle por celda")
    lin.append("")
    lin.append("| Base | Gen | Ventanas | (a) eficientes | (b) aciertos `+` | "
               "(c) cualquier hebra | (d) sin acierto | (e) multiple | Filas | Origen |")
    lin.append("|" + "---|" * 10)
    for base, por_gen in resumen["celdas"].items():
        for gen, c in por_gen.items():
            lin.append(
                f"| `{base}` | {gen} | {c['ventanas_total']} | {c['eficientes_por_ventana']} "
                f"| {c['aciertos_mas_total']} | {c['aciertos_cualquier_hebra_total']} "
                f"| {c['eficientes_sin_acierto']} "
                f"| {c['eficientes_con_acierto_multiple_en_una_ref']} "
                f"| {c['referencias_con_fila']} | {c['origen']} |")
    return "\n".join(lin)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("contar", help="aplica la regla del original a la matriz gen x base")
    c.add_argument("--gen", action="append", metavar="NOMBRE=TSV",
                   help="TSV por ventana del port, uno por gen")
    c.add_argument("--base", action="append", metavar="NOMBRE=FASTA", default=None,
                   help="base contra la que enumerar aciertos localmente")
    c.add_argument("--aciertos", action="append", metavar="BASE:GEN=SALIDA_BOWTIE", default=None,
                   help="aciertos ya calculados por Bowtie")
    c.add_argument("--mm", type=int, default=0, choices=(0, 1),
                   help="desajustes permitidos en la enumeracion local (bowtie -v)")
    c.add_argument("--declarado", action="append", metavar="GEN=N", default=None,
                   help="sobrescribe el vector declarado")
    c.add_argument("--exigir-identidad", metavar="BASE", default=None,
                   help="falla si contra esa base alguna ventana eficiente no pega en `+`")
    c.add_argument("--json", default=None)
    c.add_argument("--md", default=None)
    c.set_defaults(func=cmd_contar)

    v = sub.add_parser("ventanas", help="FASTA de ventanas para Bowtie")
    v.add_argument("--tsv", required=True)
    v.add_argument("--salida", required=True)
    v.set_defaults(func=cmd_ventanas)

    r = sub.add_parser("revcomp", help="complemento reverso de un FASTA")
    r.add_argument("--fasta", required=True)
    r.add_argument("--salida", required=True)
    r.set_defaults(func=cmd_revcomp)

    a = ap.parse_args(argv)
    return a.func(a)


if __name__ == "__main__":
    sys.exit(main())
