"""El contrato de datos del grafico. Una sola fuente, dos dibujantes.

Por que existe este modulo y no se dibuja directo: el repositorio ya tiene la regla de
eficiencia escrita tres veces (`sifi_core._terminal_rule`, `sifi_core.apply_rules` y
`M7/grilla_parametros.eficientes`), sostenidas por tests de coherencia. No se agrega una
cuarta copia de nada. Aca se calculan los datos del grafico una vez y se emiten como JSON;
el dibujo interactivo (`estatico/app.js`) y el informe estatico
(`tools/sifi21_port/informe_html.py`, que ya esta verificado y no se toca) son dos
consumidores del mismo contrato.

Las tres curvas, que son tres preguntas distintas y conviene no confundir:

  solapamiento   cuantos siRNA eficientes se superponen a cada posicion del ARNm. Es la
                 curva roja del «RNAi design plot» del si-Fi21 original
                 (`show_plot.py:99-178`, `np.bincount(eff_sirna_plot)`). Su maximo posible
                 es el tamano de la ventana. Esta es la curva de PARIDAD: la que el
                 investigador reconoce, y la que se reprodujo tramo por tramo contra el
                 programa (ocho tramos, maximo 9 en 150-156, luego 8 en 287-297 en
                 `ATPaseD_Dm`; ver `research/ola2/W5_secuencias_epilab/sifi21_reproduccion.md`
                 lineas 85-89).

**Cuidado con el ancho de cobertura, que no es el mismo en todas las curvas de este
problema.** Hay dos objetos distintos y se parecen lo suficiente para confundirlos:

  - la curva roja del si-Fi21 original asigna **21** posiciones a cada ventana de 21 nt. Es
    la que calcula `solapamiento` y la que esta verificada: con 21 la meseta de altura 9
    cae en 150-156, la de 8 en 287-297 y la linea azul queda plana en 21, que son las tres
    marcas que se leyeron de la pantalla; con 20 las tres caen un nucleotido antes `[M]`
    (`research/ola5/N2_ancho_de_cobertura/`);
  - la curva historica que EPILAB guarda en su base asigna **20** `[R]`, y su contador
    identifica siRNAs por los incrementos positivos de esa curva, lo que esconde una
    ventana eficiente cada vez que otra termina donde esa empieza. Con 20 —y solo con 20—
    se reproducen los cuatro conteos de la planilla `[M]`
    (`research/ola5/N1_regla_de_conteo/`).

O sea que el 20 no corrige a este modulo: pertenece a otra curva. Por eso el ancho es un
parametro con nombre propio y no se deriva del tamano del siRNA adentro de la funcion.

  todos          cuantos siRNA cualesquiera se superponen a cada posicion. Es la linea azul
                 del original, plana en el tamano de la ventana salvo en los dos bordes.

  densidad       cuantos siRNA eficientes tendria una region de largo L CENTRADA en esa
                 posicion. No existe en el original: es el aporte nuestro, porque es
                 literalmente la variable de decision —elegir region es elegir un punto de
                 esta curva— y esta indexada por el centro por decision D14.

El algoritmo de `densidad` es el de `informe_html.py:577-585`, con suma de prefijos para que
sea lineal y no cuadratica. `test_perfil.py` verifica que las dos implementaciones coincidan
array por array: si alguien cambia una, el test falla.
"""

from __future__ import annotations


def solapamiento(posiciones_eficientes, largo: int, ancho_cobertura: int) -> list[int]:
    """Curva roja del original: cuantos siRNA eficientes cubren cada posicion.

    Una ventana que empieza en `p` (1-based) cubre `p .. p + ancho_cobertura - 1`. Se
    acumula por diferencias y se integra, para no pagar `ancho_cobertura` operaciones por
    ventana.

    `ancho_cobertura` **no** es el tamano del siRNA aunque para esta curva valgan lo mismo:
    para la curva del si-Fi21 original va 21, y la curva historica de EPILAB usa 20 (ver el
    encabezado del modulo). Quien llama elige, y `contrato` pasa `size` porque esta es la
    curva de paridad.
    """
    delta = [0] * (largo + 2)
    for p in posiciones_eficientes:
        ini = max(1, p)
        fin = min(largo, p + ancho_cobertura - 1)
        if ini > fin:
            continue
        delta[ini] += 1
        delta[fin + 1] -= 1
    out, acc = [], 0
    for x in range(1, largo + 1):
        acc += delta[x]
        out.append(acc)
    return out


def todos(n_ventanas: int, largo: int, size: int) -> list[int]:
    """Linea azul del original: cuantos siRNA cualesquiera cubren cada posicion.

    En el interior del gen vale `size`; baja en los dos bordes porque ahi no caben todas las
    ventanas. Se calcula con la misma rutina que el solapamiento sobre todas las ventanas,
    en vez de asumir la meseta, para que los bordes sean los de verdad.
    """
    return solapamiento(range(1, n_ventanas + 1), largo, size)


def densidad(posiciones_eficientes, n_ventanas: int, largo_region: int) -> list[int]:
    """Cuantos eficientes caen en la region de largo `largo_region` centrada en cada x.

    Replica `informe_html.py:577-585`. Cerca de los extremos la region se recorta contra el
    borde del gen, asi que el valor baja de verdad —hay menos ventanas alcanzables ahi— y
    quien dibuja marca ese tramo distinto (ver `centro_min`/`centro_max` en el contrato).
    """
    efic = set(posiciones_eficientes)
    pre = [0] * (n_ventanas + 1)
    for i in range(1, n_ventanas + 1):
        pre[i] = pre[i - 1] + (1 if i in efic else 0)
    media = (largo_region - 1) // 2
    out = []
    for x in range(1, n_ventanas + 1):
        ini = max(1, x - media)
        fin = min(n_ventanas, x - media + largo_region - 1)
        out.append(pre[fin] - pre[ini - 1])
    return out


def contrato(*, nombre, ventanas, resumen, largo, size, largo_region, mejor,
             off_perfecto=None, off_mm1=None, bandas=None, etiqueta="") -> dict:
    """El JSON que consume cualquier dibujante.

    `off_perfecto` y `off_mm1` son listas de posiciones o **None**. None no es lo mismo que
    lista vacia y el contrato lo distingue a proposito: vacia significa «se midio y no hay»,
    None significa «no se midio». Dibujar un carril vacio cuando nadie midio es el error que
    `informe_html.py` ya evita escribiendo «sin medir» en la tira.
    """
    efic = [w.pos for w in ventanas if w.is_efficient]
    media = (largo_region - 1) // 2
    dens = densidad(efic, len(ventanas), largo_region)

    return {
        "nombre": nombre,
        "largo": largo,
        "n_ventanas": len(ventanas),
        "size": size,
        "largo_region": largo_region,
        "etiqueta": etiqueta,
        # curvas
        "solapamiento": solapamiento(efic, largo, size),
        "todos": todos(len(ventanas), largo, size),
        "densidad": dens,
        "dens_max": max(dens) if dens else 0,
        # donde la region de largo_region entra completa; afuera la curva va punteada
        "centro_min": 1 + media,
        "centro_max": max(1 + media, len(ventanas) - largo_region + 1 + media),
        # marcas
        "eficientes": efic,
        "off_perfecto": sorted(off_perfecto) if off_perfecto is not None else None,
        "off_mm1": sorted(off_mm1) if off_mm1 is not None else None,
        "bandas": bandas or [],
        "mejor": mejor,
        "resumen": resumen,
    }
