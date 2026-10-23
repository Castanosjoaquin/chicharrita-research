"""Cuanta evidencia hace falta para distinguir el modo fiel del corregido.

Por que existe. El investigador pidio «conservar ambos modelos y pensar que
evidencia experimental permitiria compararlos» `[R]`. La validacion retrospectiva
preregistrada de C9 ya los comparo sobre los 29 siRNA de Cedden 2025 y no los
distinguio: rho = +0,142 con IC95 [-0,247, +0,492] en modo fiel y rho = +0,024
[-0,356, +0,397] en corregido `[M]`. Este modulo contesta la pregunta cuantitativa
que queda abierta: **con cuantos siRNA con eficacia medida se distinguirian**.

Las dos correlaciones son dependientes --los dos modos se evaluan sobre las mismas
ventanas, y por C1 de `CAMBIOS.md` el corregido es un subconjunto estricto del
fiel-- asi que la comparacion no es de dos muestras independientes. Y con n = 29
ninguna formula asintotica es creible. De ahi el remuestreo: la poblacion madre es
el propio conjunto de Cedden, se sacan muestras con reposicion de tamano n y se
cuenta cuantas veces una prueba de permutacion rechaza.

Las tres piezas, y que pregunta contesta cada una:
  1. `n_minimo_remuestreo`: cuantos siRNA hacen falta para distinguir los dos modos
     **replicando el diseno de Cedden**, o sea con su misma tasa de discordancia
     entre modos y su mismo desenlace. Contesta la pregunta tal como esta hecha.
  2. `n_por_grupo`: cuantos siRNA por brazo hacen falta en un ensayo prospectivo que
     **elige** siRNA discordantes contra concordantes-eficientes, con el
     silenciamiento del transcrito como variable de respuesta. Es el diseno que
     discrimina, y su cuenta no es una correlacion sino un contraste de dos grupos.
  3. `n_por_grupo_tost`: lo mismo cuando la conclusion buscada es «silencian igual»,
     que es una afirmacion de equivalencia y no se puede sostener con un no rechazo.

Lo que este modulo NO hace. No ajusta ningun modelo, no toca el motor de eficiencia
y no necesita secuencias: su unico insumo es la tabla de 29 filas con predictor y
desenlace que dejo C9, que ya esta en `research/` y no tiene datos de EPILAB.

Una limitacion que gobierna la lectura de todo lo que sale de aca: en las 29 filas de
Cedden hay **un solo siRNA discordante** entre los dos modos (`si778`). El remuestreo
reproduce ese unico desenlace cada vez que lo sortea, asi que sirve para contestar
«cuanto mas de este mismo dato haria falta» y **no** para estimar la potencia de un
diseno que enriquezca discordantes. Esa segunda cuenta es la de las piezas 2 y 3, con
sus supuestos declarados.

Uso:
    python potencia_dos_modelos.py observado
    python potencia_dos_modelos.py potencia --b 2000 --perm 999
    python potencia_dos_modelos.py ensayo
    python potencia_dos_modelos.py todo --salida ../resultados/potencia.json
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Sequence

import numpy as np
from scipy import integrate
from scipy.stats import chi2, mannwhitneyu, nct, norm, rankdata, t as t_dist

RAIZ = Path(__file__).resolve().parents[3]
TSV_C9_POR_DEFECTO = (
    RAIZ / "ola3" / "C9_sensibilidad_umbral" / "resultados" / "validacion_31sirna.tsv"
)


@dataclass
class Datos:
    """Las tres columnas que hacen falta: los dos predictores y el desenlace."""

    nombres: Sequence[str] | None
    fiel: np.ndarray
    corregido: np.ndarray
    hr: np.ndarray


@dataclass
class ResultadoPotencia:
    n: int
    potencia: float
    ic95: tuple[float, float]
    b: int
    n_perm: int
    alpha: float


@dataclass
class ResultadoNMinimo:
    n: int | None
    potencia: float
    objetivo: float
    curva: list[ResultadoPotencia] = field(default_factory=list)


def cargar_cedden(ruta: Path = TSV_C9_POR_DEFECTO) -> Datos:
    """Lee la tabla de 29 siRNA que dejo la validacion retrospectiva de C9."""
    nombres: list[str] = []
    fiel: list[float] = []
    corregido: list[float] = []
    hr: list[float] = []
    with open(ruta, newline="", encoding="utf-8") as fh:
        for fila in csv.DictReader(fh, delimiter="\t"):
            nombres.append(fila["nombre"])
            fiel.append(float(fila["eficiente_fiel"]))
            corregido.append(float(fila["eficiente_corregido"]))
            hr.append(float(fila["hr"]))
    return Datos(
        nombres=nombres,
        fiel=np.asarray(fiel, dtype=float),
        corregido=np.asarray(corregido, dtype=float),
        hr=np.asarray(hr, dtype=float),
    )


def n_discordantes(datos: Datos) -> int:
    """Cuantos siRNA clasifica distinto cada modo. Gobierna toda la potencia."""
    return int(np.count_nonzero(datos.fiel != datos.corregido))


def rho_spearman(x: np.ndarray, y: np.ndarray) -> float:
    """Correlacion de rangos. Devuelve nan si alguna variable es constante.

    Con un predictor binario equivale a una comparacion de rangos entre los dos
    grupos, que es como lo define el pre-registro de C9.
    """
    rx = rankdata(x)
    ry = rankdata(y)
    if np.ptp(rx) == 0 or np.ptp(ry) == 0:
        return float("nan")
    rx = rx - rx.mean()
    ry = ry - ry.mean()
    return float(rx @ ry / math.sqrt((rx @ rx) * (ry @ ry)))


def _rho_binario_desde_suma(
    suma: np.ndarray, marcados: np.ndarray, n: int, norma_y: float
) -> np.ndarray:
    """rho de un predictor binario, a partir de la suma de rangos de los marcados.

    Con x binario de m unos, la covarianza con los rangos centrados del desenlace
    es la suma de esos rangos sobre las posiciones marcadas, y la desviacion de x
    es sqrt(m - m^2/n). Escribirlo asi deja la permutacion en dos vectores y evita
    recalcular rangos: lo que se intercambia son filas, no el desenlace.

    Un predictor constante (m = 0 o m = n) no tiene rho; se devuelve 0, que es el
    valor neutro para la diferencia entre modos y equivale a «este modo no ordena
    nada en esta muestra».
    """
    m = marcados.astype(float)
    var_x = m - (m**2) / n
    with np.errstate(divide="ignore", invalid="ignore"):
        rho = suma / np.sqrt(var_x * norma_y**2)
    return np.where(var_x > 0, rho, 0.0)


@dataclass
class _Intercambio:
    """Todo lo que hace falta para evaluar la diferencia de los dos rho al intercambiar.

    Existe para que la version sorteada de la prueba (`p_permutacion`) y la version
    exhaustiva (`p_exacto_enumerado`) compartan la preparacion y el estadistico, que
    es donde esta la unica parte delicada: los rangos del desenlace se calculan una
    sola vez y lo que cambia entre aleatorizaciones son solo las filas discordantes.
    """

    n: int
    ry_d: np.ndarray
    a: np.ndarray
    b: np.ndarray
    suma_fija: float
    k_fija: int
    norma_y: float

    @property
    def k(self) -> int:
        """Cuantas filas discordantes tiene la muestra."""
        return int(self.a.size)

    def stat(self, vals_f: np.ndarray, vals_c: np.ndarray) -> np.ndarray:
        suma_f = self.suma_fija + vals_f @ self.ry_d
        suma_c = self.suma_fija + vals_c @ self.ry_d
        m_f = self.k_fija + vals_f.sum(axis=-1).astype(int)
        m_c = self.k_fija + vals_c.sum(axis=-1).astype(int)
        rho_f = _rho_binario_desde_suma(
            np.atleast_1d(suma_f), np.atleast_1d(m_f), self.n, self.norma_y
        )
        rho_c = _rho_binario_desde_suma(
            np.atleast_1d(suma_c), np.atleast_1d(m_c), self.n, self.norma_y
        )
        return rho_f - rho_c


def _preparar_intercambio(
    fiel: np.ndarray, corregido: np.ndarray, hr: np.ndarray
) -> _Intercambio | None:
    """Devuelve None cuando no hay nada que aleatorizar, y entonces el p es 1.

    Son dos casos: que los dos modos clasifiquen igual todas las filas, y que el
    desenlace sea constante.
    """
    disc = np.flatnonzero(fiel != corregido)
    if disc.size == 0:
        return None
    ry = rankdata(hr)
    if np.ptp(ry) == 0:
        return None
    ry = ry - ry.mean()
    concordante = np.ones(len(hr), dtype=bool)
    concordante[disc] = False
    return _Intercambio(
        n=len(hr),
        ry_d=ry[disc],
        a=fiel[disc],
        b=corregido[disc],
        suma_fija=float(ry[concordante] @ fiel[concordante]),
        k_fija=int(fiel[concordante].sum()),
        norma_y=math.sqrt(float(ry @ ry)),
    )


def p_permutacion(
    fiel: np.ndarray,
    corregido: np.ndarray,
    hr: np.ndarray,
    n_perm: int = 999,
    rng: np.random.Generator | None = None,
) -> float:
    """p a dos colas para la diferencia de los dos rho dependientes.

    La hipotesis nula es la nula fuerte de intercambiabilidad: que la etiqueta
    «fiel» o «corregido» pegada a cada clasificacion es arbitraria respecto del
    desenlace. La aleatorizacion correspondiente es intercambiar, siRNA por siRNA y
    con probabilidad 1/2, los dos valores del predictor. Solo las filas discordantes
    cambian al intercambiar, asi que la prueba esta conducida por ellas: si no hay
    discordantes en la muestra, no hay nada que aleatorizar y p = 1.

    Es la prueba adecuada para dos correlaciones dependientes con el mismo
    desenlace y no supone normalidad ni n grande, que es lo que descartaba la
    formula asintotica con n = 29.
    """
    rng = np.random.default_rng() if rng is None else rng
    prep = _preparar_intercambio(fiel, corregido, hr)
    if prep is None:
        return 1.0

    d_obs = float(prep.stat(prep.a, prep.b)[0])
    intercambia = rng.random((n_perm, prep.k)) < 0.5
    d_perm = prep.stat(
        np.where(intercambia, prep.b, prep.a), np.where(intercambia, prep.a, prep.b)
    )
    # El observado entra a la distribucion de referencia (p nunca es 0).
    extremos = int(np.count_nonzero(np.abs(d_perm) >= abs(d_obs) - 1e-12))
    return (extremos + 1) / (n_perm + 1)


def p_exacto_enumerado(
    fiel: np.ndarray, corregido: np.ndarray, hr: np.ndarray, k_max: int = 22
) -> float:
    """El p de la prueba enumerando las 2^k aleatorizaciones, sin sorteo.

    Con pocas filas discordantes el conjunto de aleatorizacion es chico y se puede
    recorrer entero, de modo que el p no tiene error de simulacion. Es lo que hace
    visible el techo de esta prueba: con k discordantes el p mas chico alcanzable es
    2/2^k --la asignacion observada y su espejo-- asi que con k < 6 **ningun dato
    puede dar p <= 0,05**, por mucho que crezca el n total.
    """
    prep = _preparar_intercambio(fiel, corregido, hr)
    if prep is None:
        return 1.0
    if prep.k > k_max:
        raise ValueError(f"{prep.k} discordantes: 2^k no es enumerable, usar p_permutacion")

    todas = ((np.arange(2**prep.k)[:, None] >> np.arange(prep.k)) & 1).astype(bool)
    d = prep.stat(np.where(todas, prep.b, prep.a), np.where(todas, prep.a, prep.b))
    d_obs = float(d[0])  # la fila 0 es «ningun intercambio», o sea lo observado
    return float(np.count_nonzero(np.abs(d) >= abs(d_obs) - 1e-12) / 2**prep.k)


def k_minimo_para_rechazar(alpha: float = 0.05) -> int:
    """Cuantos siRNA discordantes hacen falta para que la prueba pueda rechazar.

    Cota combinatoria, independiente del n total y del desenlace: el p mas chico que
    el conjunto de aleatorizacion admite es 2/2^k, asi que hace falta 2^k >= 2/alpha.
    """
    return int(math.ceil(math.log2(2.0 / alpha)))


def pool_discordantes_por_defecto(datos: Datos) -> np.ndarray:
    """Los desenlaces de los siRNA que el modo fiel marca como eficientes.

    Es el reservorio con el que se corrige la pseudo-replicacion del remuestreo
    (ver `potencia_remuestreo`): la clase discordante es, por construccion, un
    subconjunto de los que el fiel marca, asi que es el reservorio observado mas
    cercano que tiene varianza propia.
    """
    return datos.hr[datos.fiel > 0]


def potencia_remuestreo(
    datos: Datos,
    n: int,
    b: int = 1000,
    n_perm: int = 499,
    alpha: float = 0.05,
    rng: np.random.Generator | None = None,
    pool_discordantes: np.ndarray | None = None,
) -> ResultadoPotencia:
    """Fraccion de muestras de tamano n en las que la prueba rechaza.

    La poblacion madre es la tabla de Cedden tal cual: se sortean n filas con
    reposicion, de modo que la tasa de discordancia entre modos, la proporcion de
    negativos y la restriccion de rango del desenlace son las del dato real.

    **Pseudo-replicacion, y como se corrige.** En esa tabla hay un solo siRNA
    discordante, asi que un remuestreo sin mas sortea copias del mismo desenlace: la
    clase discordante queda con varianza cero y su aporte a la diferencia entre los
    dos rho tiene siempre el mismo signo. Eso **sobreestima la potencia**, porque en
    un conjunto real algunos discordantes apuntarian al otro lado. Con
    `pool_discordantes` se le vuelve a dar varianza: a cada fila discordante sorteada
    se le redibuja el desenlace de ese reservorio. La version sin reservorio es un
    piso optimista; la version con reservorio es la estimacion honesta.
    """
    rng = np.random.default_rng() if rng is None else rng
    n0 = len(datos.hr)
    rechazos = 0
    for _ in range(b):
        idx = rng.integers(0, n0, n)
        fiel, corregido, hr = datos.fiel[idx], datos.corregido[idx], datos.hr[idx]
        if pool_discordantes is not None and len(pool_discordantes):
            disc = fiel != corregido
            k = int(np.count_nonzero(disc))
            if k:
                hr = hr.copy()
                hr[disc] = rng.choice(pool_discordantes, size=k, replace=True)
        p = p_permutacion(fiel, corregido, hr, n_perm=n_perm, rng=rng)
        rechazos += int(p <= alpha)
    pot = rechazos / b
    # Wilson, por la misma razon por la que C9 reporta Wilson en la curva PR.
    z = 1.959963985
    centro = (pot + z * z / (2 * b)) / (1 + z * z / b)
    radio = (z / (1 + z * z / b)) * math.sqrt(pot * (1 - pot) / b + z * z / (4 * b * b))
    return ResultadoPotencia(
        n=n,
        potencia=pot,
        ic95=(max(0.0, centro - radio), min(1.0, centro + radio)),
        b=b,
        n_perm=n_perm,
        alpha=alpha,
    )


def n_minimo_remuestreo(
    datos: Datos,
    objetivo: float = 0.8,
    b: int = 1000,
    n_perm: int = 499,
    alpha: float = 0.05,
    rng: np.random.Generator | None = None,
    n_max: int = 200_000,
    pool_discordantes: np.ndarray | None = None,
) -> ResultadoNMinimo:
    """Busca el n mas chico con potencia >= objetivo: duplica y despues biseca."""
    rng = np.random.default_rng() if rng is None else rng
    curva: list[ResultadoPotencia] = []
    n = len(datos.hr)
    alcanzado: ResultadoPotencia | None = None

    def potencia_en(n: int) -> ResultadoPotencia:
        return potencia_remuestreo(
            datos,
            n=n,
            b=b,
            n_perm=n_perm,
            alpha=alpha,
            rng=rng,
            pool_discordantes=pool_discordantes,
        )

    while n <= n_max:
        res = potencia_en(n)
        curva.append(res)
        if res.potencia >= objetivo:
            alcanzado = res
            break
        n *= 2
    if alcanzado is None:
        return ResultadoNMinimo(n=None, potencia=curva[-1].potencia, objetivo=objetivo, curva=curva)

    lo = alcanzado.n // 2
    hi = alcanzado.n
    mejor = alcanzado
    while hi - lo > max(1, hi // 20):
        medio = (lo + hi) // 2
        res = potencia_en(medio)
        curva.append(res)
        if res.potencia >= objetivo:
            hi = medio
            mejor = res
        else:
            lo = medio
    return ResultadoNMinimo(n=mejor.n, potencia=mejor.potencia, objetivo=objetivo, curva=curva)


def potencia_dos_grupos(delta: float, sd: float, n_por_brazo: int, alpha: float = 0.05) -> float:
    """Potencia exacta de la t de dos muestras, en las mismas unidades que delta y sd.

    Es la cuenta del ensayo prospectivo: dos brazos de siRNA --discordantes y
    concordantes-eficientes-- y el silenciamiento del transcrito como respuesta.
    """
    if n_por_brazo < 2:
        return 0.0
    df = 2 * n_por_brazo - 2
    ncp = delta / (sd * math.sqrt(2.0 / n_por_brazo))
    crit = t_dist.ppf(1 - alpha / 2, df)
    return float(1 - nct.cdf(crit, df, ncp) + nct.cdf(-crit, df, ncp))


def _n_mas_chico(potencia_en, objetivo: float, n_max: int) -> int:
    """El n por brazo mas chico cuya potencia alcanza el objetivo.

    La potencia de las dos pruebas de brazos fijos crece con n, asi que recorrerla de
    abajo hacia arriba devuelve el minimo y no hace falta bisecar.
    """
    for n in range(2, n_max + 1):
        if potencia_en(n) >= objetivo:
            return n
    raise ValueError("no se alcanza el objetivo dentro de n_max")


def n_por_grupo(
    delta: float, sd: float, alpha: float = 0.05, objetivo: float = 0.8, n_max: int = 100_000
) -> int:
    """El n por brazo mas chico que alcanza el objetivo de potencia."""
    return _n_mas_chico(lambda n: potencia_dos_grupos(delta, sd, n, alpha), objetivo, n_max)


def potencia_tost(margen: float, sd: float, n_por_brazo: int, alpha: float = 0.05) -> float:
    """Potencia de la prueba de equivalencia (TOST) con diferencia verdadera nula.

    Hace falta porque el resultado «los discordantes silencian como los
    concordantes» es una equivalencia: no rechazar una diferencia no es lo mismo que
    mostrar que no la hay, y con muestras chicas lo primero pasa casi siempre.

    Se integra sobre la distribucion de la desviacion estandar muestral en vez de
    simular, para que el numero sea reproducible sin semilla.
    """
    if n_por_brazo < 2:
        return 0.0
    df = 2 * n_por_brazo - 2
    crit = t_dist.ppf(1 - alpha, df)
    margen_tipificado = margen / (sd * math.sqrt(2.0 / n_por_brazo))

    def integrando(u: float) -> float:
        lim = margen_tipificado - crit * u
        if lim <= 0:
            return 0.0
        prob = norm.cdf(lim) - norm.cdf(-lim)
        # densidad de u = s/sd, con df*u^2 ~ chi2_df
        dens = chi2.pdf(df * u * u, df) * 2 * df * u
        return prob * dens

    valor, _ = integrate.quad(integrando, 1e-9, margen_tipificado / crit, limit=200)
    return float(min(max(valor, 0.0), 1.0))


def n_por_grupo_tost(
    margen: float, sd: float, alpha: float = 0.05, objetivo: float = 0.8, n_max: int = 100_000
) -> int:
    """El n por brazo mas chico que alcanza el objetivo con la prueba de equivalencia."""
    return _n_mas_chico(lambda n: potencia_tost(margen, sd, n, alpha), objetivo, n_max)


def potencia_dos_grupos_mwu(
    delta: float,
    sd: float,
    n_por_brazo: int,
    alpha: float = 0.05,
    b: int = 4000,
    rng: np.random.Generator | None = None,
) -> float:
    """Sensibilidad no parametrica de `potencia_dos_grupos`, por simulacion.

    El porcentaje de silenciamiento esta acotado entre 0 y 100 y suele ser asimetrico,
    asi que conviene saber cuanto se pierde si el analisis es por rangos.
    """
    rng = np.random.default_rng() if rng is None else rng
    rechazos = 0
    for _ in range(b):
        tratado = rng.normal(delta, sd, n_por_brazo)
        control = rng.normal(0.0, sd, n_por_brazo)
        try:
            p = mannwhitneyu(tratado, control, alternative="two-sided").pvalue
        except ValueError:
            continue
        rechazos += int(p <= alpha)
    return rechazos / b


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("accion", choices=["observado", "potencia", "ensayo", "todo"])
    ap.add_argument("--tsv", type=Path, default=TSV_C9_POR_DEFECTO)
    ap.add_argument("--b", type=int, default=1000, help="muestras de remuestreo por n")
    ap.add_argument("--perm", type=int, default=499, help="permutaciones por muestra")
    ap.add_argument("--alpha", type=float, default=0.05)
    ap.add_argument("--objetivo", type=float, default=0.8)
    ap.add_argument("--semilla", type=int, default=20261023)
    ap.add_argument("--salida", type=Path, default=None)
    args = ap.parse_args(argv)

    rng = np.random.default_rng(args.semilla)
    datos = cargar_cedden(args.tsv)
    salida: dict = {
        "insumo": (
            args.tsv.relative_to(RAIZ.parent).as_posix()
            if args.tsv.is_absolute()
            else args.tsv.as_posix()
        ),
        "semilla": args.semilla,
        "alpha": args.alpha,
        "objetivo_potencia": args.objetivo,
    }

    if args.accion in ("observado", "todo"):
        rho_f = rho_spearman(datos.fiel, datos.hr)
        rho_c = rho_spearman(datos.corregido, datos.hr)
        p = p_permutacion(datos.fiel, datos.corregido, datos.hr, n_perm=9999, rng=rng)
        salida["observado"] = {
            "n": len(datos.hr),
            "rho_fiel": round(rho_f, 4),
            "rho_corregido": round(rho_c, 4),
            "diferencia": round(rho_f - rho_c, 4),
            "discordantes": n_discordantes(datos),
            "nombres_discordantes": [
                nombre
                for nombre, f, c in zip(datos.nombres or [], datos.fiel, datos.corregido)
                if f != c
            ],
            "marcados_fiel": int(datos.fiel.sum()),
            "marcados_corregido": int(datos.corregido.sum()),
            "p_permutacion_9999": round(p, 4),
            "p_exacto_enumerado": round(
                p_exacto_enumerado(datos.fiel, datos.corregido, datos.hr), 4
            ),
            "k_minimo_discordantes_para_rechazar": k_minimo_para_rechazar(args.alpha),
            "tasa_discordancia": round(n_discordantes(datos) / len(datos.hr), 4),
            "n_para_esa_cantidad_de_discordantes_en_promedio": math.ceil(
                k_minimo_para_rechazar(args.alpha) * len(datos.hr) / max(1, n_discordantes(datos))
            ),
        }
        print(json.dumps(salida["observado"], indent=1, ensure_ascii=False))

    if args.accion in ("potencia", "todo"):
        res = n_minimo_remuestreo(
            datos,
            objetivo=args.objetivo,
            b=args.b,
            n_perm=args.perm,
            alpha=args.alpha,
            rng=rng,
        )
        pool = pool_discordantes_por_defecto(datos)
        res_pool = n_minimo_remuestreo(
            datos,
            objetivo=args.objetivo,
            b=args.b,
            n_perm=args.perm,
            alpha=args.alpha,
            rng=rng,
            pool_discordantes=pool,
        )

        def curva(r: ResultadoNMinimo) -> list[dict]:
            return [
                {
                    "n": punto.n,
                    "potencia": punto.potencia,
                    "ic95": [round(punto.ic95[0], 4), round(punto.ic95[1], 4)],
                }
                for punto in sorted(r.curva, key=lambda punto: punto.n)
            ]

        ultimo = res.curva[-1]
        salida["remuestreo"] = {
            "n_minimo": res.n,
            "potencia_en_n_minimo": res.potencia,
            "curva": curva(res),
            "b": ultimo.b,
            "permutaciones": ultimo.n_perm,
            "sensibilidad_con_varianza_en_discordantes": {
                "que_es": (
                    "mismo procedimiento, pero redibujando el desenlace de cada fila "
                    "discordante sorteada del reservorio de los que el modo fiel marca "
                    "eficientes. Corrige la pseudo-replicacion del unico discordante "
                    "observado, que deja a esa clase con varianza cero"
                ),
                "reservorio_hr": [round(float(v), 3) for v in sorted(pool)],
                "n_minimo": res_pool.n,
                "potencia_en_n_minimo": res_pool.potencia,
                "curva": curva(res_pool),
            },
        }
        print(json.dumps(salida["remuestreo"], indent=1, ensure_ascii=False))

    if args.accion in ("ensayo", "todo"):
        sds = [15.0, 20.0, 25.0]
        deltas = [20.0, 30.0, 40.0]
        tabla = []
        for sd in sds:
            for delta in deltas:
                tabla.append(
                    {
                        "sd_pp": sd,
                        "delta_pp": delta,
                        "n_por_brazo_alpha05": n_por_grupo(delta, sd, 0.05, args.objetivo),
                        "n_por_brazo_alpha025": n_por_grupo(delta, sd, 0.025, args.objetivo),
                    }
                )
        equivalencia = [
            {
                "sd_pp": sd,
                "margen_pp": margen,
                "n_por_brazo": n_por_grupo_tost(margen, sd, 0.05, args.objetivo),
            }
            for sd in sds
            for margen in [10.0, 15.0, 20.0]
        ]
        mwu = [
            {
                "sd_pp": 20.0,
                "delta_pp": delta,
                "n_por_brazo_t": n_por_grupo(delta, 20.0, 0.05, args.objetivo),
                "potencia_mwu_en_ese_n": round(
                    potencia_dos_grupos_mwu(
                        delta, 20.0, n_por_grupo(delta, 20.0, 0.05, args.objetivo), rng=rng
                    ),
                    3,
                ),
            }
            for delta in deltas
        ]
        salida["ensayo"] = {
            "diferencia": tabla,
            "equivalencia_tost": equivalencia,
            "sensibilidad_no_parametrica": mwu,
        }
        print(json.dumps(salida["ensayo"], indent=1, ensure_ascii=False))

    if args.salida:
        args.salida.parent.mkdir(parents=True, exist_ok=True)
        args.salida.write_text(json.dumps(salida, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"escrito: {args.salida}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
