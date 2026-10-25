"""D47: la exposicion ecologica y la senal de conservacion son dos ejes, y el motor no los combina.

Por que existe este modulo. El peso por referencia de **D18** —maiz 1,00, *Harmonia
axyridis* 0,80, *Apis mellifera* 0,80, *Homalodisca vitripennis* 0,60, *Folsomia
candida* 0,40— cumple dos funciones a la vez: dice cuanto importa que el ARNdc toque a
ese organismo (exposicion) y hace de sustituto medible de la conservacion entre
cicadelidos. El investigador pidio separarlas `[R]`, y tienen **signo opuesto**: que una
region este conservada en un cicadelido emparentado es informacion util sobre que la
region es funcional; que un organismo este expuesto es riesgo.

Que hace este modulo:

  * define **dos vectores de peso con nombres distintos**, `w_exposicion` y
    `s_conservacion`, y dos vistas disjuntas del mismo dato de off-target: el eje de
    exposicion solo ve las referencias con `w_exposicion > 0` y el de conservacion solo
    las que tienen `s_conservacion > 0`;
  * devuelve **dos numeros por region** en un `DosEjes`, cuyos campos son escalares con
    unidad (`Eje`) que **no tienen ninguna operacion en comun**: sumar, restar,
    multiplicar, dividir o comparar un eje con el otro levanta `TypeError`, y
    `float(eje)` tambien. La ponderacion final es una decision declarada del equipo o
    del laboratorio, fuera del motor;
  * no toca `ranking.py`. El orden se sigue calculando con el motor auditado de W7, al
    que se le pasa **solo** el vector de exposicion. El eje de conservacion no entra a
    ninguna funcion de orden, y `test_ejes_separados.py` lo verifica moviendolo.

La barrera es sintactica y no es una imposibilidad logica: nada impide escribir
`a.valor_de("exposicion") + b.valor_de("conservacion")`. Lo que si esta verificado es
que **este motor no lo hace**, por la prueba de invariancia: cambiar `s_conservacion`
no mueve ni un digito del orden.

Los valores de `w_exposicion` **los decide el usuario** (pedido 4 de la reunion del
lunes). Los de `PANEL_EJES` son una propuesta `[H]`; la tabla de sensibilidad de
`research/ola4/M5_dos_ejes/` mide que afirmacion se sostiene en que fraccion del
espacio de repartos, para que esa decision se tome con el numero a la vista.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

import ranking as R

MENSAJE = ("los dos ejes de D47 no se combinan en el motor: la exposicion ecologica y "
           "la senal de conservacion tienen signo opuesto y su ponderacion es una "
           "decision declarada del equipo, no una operacion de este codigo")


class Eje:
    """Un escalar con unidad. Dos ejes de nombre distinto no comparten ninguna operacion.

    Se pueden sumar y comparar dos ejes del MISMO nombre, y escalar un eje por un
    numero. Cualquier operacion entre ejes de nombre distinto —incluida la comparacion—
    levanta `TypeError`, y lo mismo `float()`, `int()` y el uso como indice.
    """

    __slots__ = ("nombre", "_valor")

    def __init__(self, nombre: str, valor: float):
        object.__setattr__(self, "nombre", nombre)
        object.__setattr__(self, "_valor", float(valor))

    def valor_de(self, nombre: str) -> float:
        """El numero, nombrando el eje. Pedirlo con otro nombre es un error."""
        if nombre != self.nombre:
            raise TypeError("este eje es '%s', no '%s'. %s" % (self.nombre, nombre, MENSAJE))
        return self._valor

    def __setattr__(self, *_a):
        raise AttributeError("Eje es inmutable")

    def __repr__(self) -> str:
        return "Eje(%r, %.6g)" % (self.nombre, self._valor)

    # -- operaciones permitidas: mismo eje con mismo eje, o escalado por un numero --
    def _mismo(self, otro, op: str):
        if isinstance(otro, Eje) and otro.nombre == self.nombre:
            return otro._valor
        raise TypeError("%s no esta definido entre %r y %r. %s" % (op, self, otro, MENSAJE))

    def __add__(self, otro):
        return Eje(self.nombre, self._valor + self._mismo(otro, "la suma"))

    def __sub__(self, otro):
        return Eje(self.nombre, self._valor - self._mismo(otro, "la resta"))

    def __mul__(self, otro):
        if isinstance(otro, (int, float)) and not isinstance(otro, bool):
            return Eje(self.nombre, self._valor * otro)
        raise TypeError("el producto no esta definido entre %r y %r. %s" % (self, otro, MENSAJE))

    def __truediv__(self, otro):
        if isinstance(otro, (int, float)) and not isinstance(otro, bool):
            return Eje(self.nombre, self._valor / otro)
        raise TypeError("el cociente no esta definido entre %r y %r. %s" % (self, otro, MENSAJE))

    __radd__ = __add__
    __rmul__ = __mul__

    def __eq__(self, otro):
        return isinstance(otro, Eje) and otro.nombre == self.nombre and otro._valor == self._valor

    def __hash__(self):
        return hash((self.nombre, self._valor))

    def __lt__(self, otro):
        return self._valor < self._mismo(otro, "la comparacion")

    def __le__(self, otro):
        return self._valor <= self._mismo(otro, "la comparacion")

    def __gt__(self, otro):
        return self._valor > self._mismo(otro, "la comparacion")

    def __ge__(self, otro):
        return self._valor >= self._mismo(otro, "la comparacion")

    # -- operaciones prohibidas: las que colapsarian el eje a un numero sin unidad --
    def __float__(self):
        raise TypeError("float(%r) no esta permitido: usa .valor_de(%r). %s"
                        % (self, self.nombre, MENSAJE))

    __int__ = __index__ = __complex__ = __float__


@dataclass(frozen=True)
class DosEjes:
    """Los dos numeros de una region. No hay ningun metodo que devuelva uno solo."""

    exposicion: Eje
    conservacion: Eje
    detalle: dict

    def __float__(self):
        raise TypeError(MENSAJE)

    def __iter__(self):
        raise TypeError(MENSAJE)

    def como_par(self) -> tuple[float, float]:
        """Los dos valores, para imprimir o tabular. No es una combinacion."""
        return (self.exposicion.valor_de("exposicion"),
                self.conservacion.valor_de("conservacion"))


# --------------------------------------------------------------------- los dos vectores

# Propuesta `[H]`, no decision. `w_exposicion` es probabilidad de contacto real con la
# formulacion en la Argentina; `s_conservacion` es informatividad filogenetica sobre
# cuan conservada esta la region entre cicadelidos. Los valores de exposicion distintos
# de *H. vitripennis* son los de D18 sin cambio: D47 parte el vector, no rejustifica el
# resto, y el barrido los mueve sobre todo el simplex igual que antes.
PANEL_EJES = {
    "GCF_902167145.1_Zm-B73-REFERENCE-NAM-5.0_rna": {
        "corto": "maiz", "w_exposicion": 1.00, "s_conservacion": 0.00,
        "motivo": "el cultivo tratado, contacto directo con la formulacion; no es cicadelido"},
    "GCF_914767665.1_icHarAxyr1.1_rna": {
        "corto": "H_axyridis", "w_exposicion": 0.80, "s_conservacion": 0.00,
        "motivo": "enemigo natural presente en el lote; no es cicadelido"},
    "GCF_003254395.2_Amel_HAv3.1_rna": {
        "corto": "A_mellifera", "w_exposicion": 0.80, "s_conservacion": 0.00,
        "motivo": "polinizador que visita el cultivo; no es cicadelido"},
    "GCF_021130785.1_UT_GWSS_2.1_rna": {
        "corto": "H_vitripennis", "w_exposicion": 0.00, "s_conservacion": 1.00,
        "motivo": "cicadelido no reportado en la Argentina: exposicion cercana a cero y "
                  "unica senal medible de conservacion entre cicadelidos del panel"},
    "GCF_002217175.1_ASM221717v1_rna": {
        "corto": "F_candida", "w_exposicion": 0.40, "s_conservacion": 0.00,
        "motivo": "fauna del suelo, exposicion indirecta; no es cicadelido"},
    "humano_rna": {
        "corto": "humano", "w_exposicion": 1.00, "s_conservacion": 0.00,
        "motivo": "no objetivo de maxima consecuencia; no es cicadelido"},
    R.DMAIDIS: {
        "corto": "D_maidis", "w_exposicion": 0.60, "s_conservacion": 0.00,
        "motivo": "el vector: on-target de los genes del insecto, y para los virales la "
                  "asimetria de signo de D5. No es senal de conservacion, es el blanco"},
}


def vector_exposicion(tau_hv: float | None = None, base: dict | None = None) -> dict[str, float]:
    """`w_exposicion` por referencia. `tau_hv` pisa el de *H. vitripennis*."""
    v = {r: (base[r] if base and r in base else d["w_exposicion"])
         for r, d in PANEL_EJES.items()}
    if tau_hv is not None:
        v["GCF_021130785.1_UT_GWSS_2.1_rna"] = float(tau_hv)
    return v


def vector_conservacion(base: dict | None = None) -> dict[str, float]:
    """`s_conservacion` por referencia."""
    return {r: (base[r] if base and r in base else d["s_conservacion"])
            for r, d in PANEL_EJES.items()}


def vista(genes: dict, pesos: dict[str, float]) -> dict:
    """El mismo dato con solo las referencias de peso no nulo en ESE eje.

    Hay que filtrar `riesgo` y no solo pasar los pesos, porque el veto, `con_off_target`
    y `buenos_limpios` de `ranking.ejes()` miran todas las referencias presentes sin
    importar su peso. Una referencia con exposicion cero no aporta riesgo por ninguna
    de las dos vias: ni al promedio ponderado ni al veto.
    """
    out = {}
    for nombre, g in genes.items():
        h = dict(g)
        h["riesgo"] = {r: v for r, v in g["riesgo"].items() if pesos.get(r, 0.0) > 0.0}
        out[nombre] = h
    return out


# ------------------------------------------------------------------- los dos numeros

def _densidad(g, ini, fin, pesos, pesos_crit, excluir, solo_eficientes) -> float:
    """Densidad ponderada de coincidencia de la region, en [0, 1]. Sin signo propio.

    Es exactamente el termino `exposicion` de `ranking.ejes()`: el promedio por ventana
    del peor acierto, normalizado por el peso maximo activo. Lo que cambia entre los dos
    ejes es QUE vector de pesos y QUE vista se le pasa, no la cuenta.
    """
    return R.ejes(g, ini, fin, pesos, pesos_crit, excluir, solo_eficientes)["exposicion"]


def conteos_por_referencia(g, ini, fin, pesos, excluir, eficiente=None) -> dict:
    """Ventanas con coincidencia por referencia y criterio dentro de la region."""
    out = {}
    for ref, crits in g["riesgo"].items():
        if ref in excluir or pesos.get(ref, 0.0) <= 0.0:
            continue
        d = {}
        for crit in R.CRITERIOS:
            v = crits[crit][ini - 1:fin]
            if v.any():
                d[crit] = int(v.sum())
                if eficiente is not None:
                    d[crit + "_eficientes"] = int((v & eficiente[ini - 1:fin]).sum())
        if d:
            out[R.corto(ref)] = d
    return out


def dos_ejes(genes: dict, cand: dict, w_exposicion: dict, s_conservacion: dict,
             pesos_crit: dict, solo_eficientes: bool = False,
             dmaidis_viral: str = "off") -> DosEjes:
    """Los dos numeros de una region, cada uno sobre su propia vista.

    `exposicion`    riesgo ecologico ponderado por `w_exposicion`, en [0, 1]. Es el
                    mismo numero que publica hoy el motor cuando `w_exposicion` son los
                    pesos de D18 (verificado en `test_ejes_separados.py`).
    `conservacion`  senal filogenetica ponderada por `s_conservacion`, en [0, 1]. **No**
                    es riesgo: un valor alto dice que la region esta conservada entre
                    cicadelidos, que es informacion sobre que la region es funcional.
    """
    gen, (ini, fin) = cand["gen"], cand["region"]
    excluir = R.excluidas_de(cand, dmaidis_viral)
    ge = vista(genes, w_exposicion)[gen]
    gc = vista(genes, s_conservacion)[gen]
    detalle = {
        "gen": gen, "region": "%d-%d" % (ini, fin),
        "n_ventanas": int(genes[gen]["presente"][ini - 1:fin].sum()),
        "eficientes": int(genes[gen]["eficiente"][ini - 1:fin].sum()),
        "exposicion_por_referencia": conteos_por_referencia(
            ge, ini, fin, w_exposicion, excluir, genes[gen]["eficiente"]),
        "conservacion_por_referencia": conteos_por_referencia(
            gc, ini, fin, s_conservacion, excluir, genes[gen]["eficiente"]),
        "vetada_por_exposicion": bool(veto(ge, ini, fin, w_exposicion, excluir)),
        "vetada_regla_actual": bool(veto(genes[gen], ini, fin, None, excluir)),
    }
    return DosEjes(
        Eje("exposicion", _densidad(ge, ini, fin, w_exposicion, pesos_crit, excluir,
                                    solo_eficientes)),
        Eje("conservacion", _densidad(gc, ini, fin, s_conservacion, pesos_crit, excluir,
                                      solo_eficientes)),
        detalle)


def veto(g: dict, ini: int, fin: int, pesos: dict | None, excluir: set) -> bool:
    """Veto de 21/21 perfecto. Con `pesos`, solo cuentan las referencias de peso no nulo.

    `pesos=None` es la regla de hoy, que es ciega al peso: cualquier referencia del panel
    veta. Con el vector de exposicion, una coincidencia con una referencia de exposicion
    cero deja de ser veto ecologico y pasa a ser senal de conservacion.
    """
    for ref, crits in g["riesgo"].items():
        if ref in excluir:
            continue
        if pesos is not None and pesos.get(ref, 0.0) <= 0.0:
            continue
        if crits["perfecto_21"][ini - 1:fin].any():
            return True
    return False


# ----------------------------------------------- D48: la alerta en lugar del booleano

class CompuertaRetirada(RuntimeError):
    """Se pidio un veredicto automatico bajo la regla de alerta de D48.

    D48 no baja la severidad: cambia la carga de la prueba. La coincidencia perfecta de
    21 nt sigue siendo una alerta fuerte, pero quien la acepta o la bloquea es una
    persona con una justificacion escrita que cita la fila de `alertas.tsv`, no este
    codigo. La forma `cascada` ES la compuerta automatica —resta 1.000 a la region
    vetada— y por eso no tiene sentido bajo esta regla.
    """


def alertas_de_region(g: dict, ini: int, fin: int, pesos: dict | None,
                      excluir: set) -> list[dict]:
    """Las coincidencias de la region por referencia y umbral de D28. **No decide nada.**

    Reemplaza el valor de retorno de `veto()` —un booleano— por la lista de lo que hay
    que justificar. Los dos umbrales van siempre los dos y estan anidados: toda ventana
    con `perfecto_21` tiene tambien un bloque perfecto de >= 19 nt. `pesos` filtra igual
    que en `veto()`: con `None` se miran todas las referencias del panel, y con el vector
    de exposicion solo las de peso no nulo.
    """
    out = []
    for ref, crits in sorted(g["riesgo"].items()):
        if ref in excluir:
            continue
        if pesos is not None and pesos.get(ref, 0.0) <= 0.0:
            continue
        v21 = crits["perfecto_21"][ini - 1:fin]
        v19 = crits["perfecto_ge19"][ini - 1:fin]
        if not v21.any() and not v19.any():
            continue
        out.append({"referencia": ref, "corto": R.corto(ref),
                    "ventanas_perfecto_21": int(v21.sum()),
                    "ventanas_perfecto_ge19": int(v19.sum()),
                    "posiciones_perfecto_21": [int(i) + ini for i in np.flatnonzero(v21)],
                    "posiciones_perfecto_ge19": [int(i) + ini for i in np.flatnonzero(v19)]})
    return out


def estado_region(g: dict, ini: int, fin: int, pesos: dict | None, excluir: set) -> dict:
    """El estado de la region bajo D48. **Nunca** devuelve «descartada» ni «aceptada».

    Los dos unicos estados que este codigo puede producir son «sin alertas» y «con
    alertas, pendiente de justificacion». La tercera y la cuarta posibilidad —aceptada
    con justificacion, bloqueada con justificacion— las escribe una persona.
    """
    al = alertas_de_region(g, ini, fin, pesos, excluir)
    n21 = sum(a["ventanas_perfecto_21"] for a in al)
    n19 = sum(a["ventanas_perfecto_ge19"] for a in al)
    return {"alertas": al, "n_referencias_con_alerta": len(al),
            "ventanas_perfecto_21": n21, "ventanas_perfecto_ge19": n19,
            "estado": "sin alertas" if not al else "con alertas, pendiente de justificacion",
            "decide": "el codigo" if not al else "el usuario",
            "vetada_regla_anterior": bool(veto(g, ini, fin, pesos, excluir))}


# ------------------------------------------------- el orden, que SOLO ve la exposicion

def barrer_exposicion(cands: list[dict], genes: dict, w_exposicion: dict, forma: str,
                      solo_eficientes: bool, muestras: int, rng, escala: str,
                      regla_veto: str = "exposicion") -> dict:
    """El barrido de W7 sobre la vista de exposicion. El eje de conservacion no entra.

    `regla_veto`  'exposicion' saca del dato las referencias de exposicion cero, de modo
                  que no vetan; 'ciego' conserva la regla de hoy, en la que cualquier
                  referencia del panel veta tenga el peso que tenga; 'alerta' es D48 y
                  **no veta nada**: devuelve `vetadas` vacio y el inventario de alertas
                  por candidato, para que la decision la tome quien la tiene que firmar.
                  Con 'alerta' la forma `cascada` levanta `CompuertaRetirada`, porque la
                  cascada es literalmente la compuerta que D48 retira.
    """
    if regla_veto == "alerta" and forma == "cascada":
        raise CompuertaRetirada(
            "la forma 'cascada' resta 1.000 a la region vetada, que es el veredicto "
            "automatico que D48 reemplaza por una alerta justificada. Bajo la regla de "
            "alerta el motor informa las alertas (ver `estado_region`) y no ordena por "
            "veto; el orden ponderado se pide con 'geometrica' o 'suma'.")
    g = vista(genes, w_exposicion) if regla_veto == "exposicion" else genes
    refs = [r for r in w_exposicion if w_exposicion[r] > 0.0]
    frec = {c["gen"]: [0] * len(cands) for c in cands}
    ordenes: dict[tuple, int] = {}
    for _ in range(muestras):
        w_ef = float(rng.random())
        wc = np.sort(rng.dirichlet(np.ones(3)))[::-1]
        pesos_crit = {c: float(x) for c, x in zip(R.CRITERIOS, wc)}
        orden = R.ordenar(cands, g, w_ef, w_exposicion, pesos_crit, forma, solo_eficientes,
                          "off", escala)
        for i, (n, _s) in enumerate(orden):
            frec[n][i] += 1
        clave = tuple(n for n, _ in orden)
        ordenes[clave] = ordenes.get(clave, 0) + 1
    pesos_veto = w_exposicion if regla_veto == "exposicion" else None
    vetadas = [] if regla_veto == "alerta" else [
        c["gen"] for c in cands
        if veto(g[c["gen"]], c["region"][0], c["region"][1], pesos_veto,
                R.excluidas_de(c, "off"))]
    alertadas = {c["gen"]: estado_region(g[c["gen"]], c["region"][0], c["region"][1],
                                         pesos_veto, R.excluidas_de(c, "off"))
                 for c in cands} if regla_veto == "alerta" else {}
    return {"frecuencia": {n: [round(100.0 * v / muestras, 1) for v in frec[n]]
                           for n in frec},
            "ordenes": sorted(({"orden": list(k), "pct": round(100.0 * v / muestras, 1)}
                               for k, v in ordenes.items()), key=lambda d: -d["pct"]),
            "vetadas": vetadas, "alertadas": alertadas, "regla_veto": regla_veto,
            "muestras": muestras, "referencias_con_exposicion": len(refs)}
