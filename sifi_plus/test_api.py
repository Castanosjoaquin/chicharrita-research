"""Las anclas de conteo, por el camino de codigo de la aplicacion.

Que prueba esto y por que importa: la interfaz no tiene que haber movido ni un numero. El port
ya esta verificado contra el programa original, pero esa verificacion corrio por
`run_sifi.py`. Si la aplicacion llama al motor de otra forma —otro default, otro orden, otra
conversion— puede dar numeros distintos y nadie se enteraria. Asi que estas verificaciones
entran por `api.correr_diseno`, que es exactamente lo que ejecuta el servidor cuando alguien
aprieta «Correr».

Las anclas, publicadas en `tools/sifi21_port/CAMBIOS.md` y
`research/ola4/M2_ventana_a_ventana/scripts/correr_pares.py`:

    RNAplfold 2.1.5 (el de si-Fi21)   fiel: 133, 32, 212, 42   corregido: 114, 25, 162, 34
    ViennaRNA 2.7.2                   fiel: 142, 39, 223, 35   corregido: 123, 30, 171, 29

Y la mas externa, que no es nuestra: los cuatro conteos que imprimio el **programa original**
con su interfaz y sus defaults, en `research/ola2/W5_secuencias_epilab/analisis/
sifi21_original_*.csv`.

Si faltan los FASTA de `work/` o el binario de RNAplfold, el bloque correspondiente se declara
**no corrido** y se dice en el resumen. Un cero tranquilizador que en realidad significa «no se
miro» es el patron que este repositorio evita a proposito.

Uso:
    python test_api.py
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import api
import complejidad
import lectura
import perfil
import proyecto

FALLAS: list[str] = []
NO_CORRIDO: list[str] = []
HECHAS = 0

W5 = api.RAIZ / "research" / "ola2" / "W5_secuencias_epilab" / "analisis"
CHECK = api.RAIZ / "work" / "sifi_check"

GENES = ["MP_MRFV", "CP_MRFV", "BicC_Dm", "ATPaseD_Dm"]

ANCLAS = {
    ("exe", "fiel"): [133, 32, 212, 42],
    ("exe", "corregido"): [114, 25, 162, 34],
    ("vienna", "fiel"): [142, 39, 223, 35],
    ("vienna", "corregido"): [123, 30, 171, 29],
}


def check(cond, etiqueta):
    global HECHAS
    HECHAS += 1
    if not cond:
        FALLAS.append(etiqueta)
        print("  FALLA  %s" % etiqueta)
    return bool(cond)


def igual(obtenido, esperado, etiqueta):
    return check(obtenido == esperado,
                 "%s: esperaba %r y dio %r" % (etiqueta, esperado, obtenido))


def leer(gen):
    p = CHECK / ("%s_full.fasta" % gen)
    if not p.is_file():
        return None
    pares = api.leer_fasta(p.read_text(encoding="utf-8"))
    return pares[0] if pares else None


def leer_ejemplo():
    """El dato de ejemplo que viaja con la carpeta: publico y sin relacion con EPILAB.

    Las pruebas del contrato entran por aca y no por `work/`, para que corran en cualquier
    maquina y no dependan de datos que no se versionan.
    """
    rutas = sorted((AQUI / "datos_ejemplo").glob("*.fasta"))
    if not rutas:
        raise FileNotFoundError("no hay datos de ejemplo en sifi_plus/datos_ejemplo")
    return api.leer_fasta(rutas[0].read_text(encoding="utf-8"))[0]


# --------------------------------------------------------------- las anclas


def test_anclas_de_conteo():
    """Los cuatro conteos, en los dos modos y con los dos motores, por el camino de la app."""
    disponibles = {m["id"]: m["disponible"] for m in api.motores()}

    for (backend, modo), esperados in sorted(ANCLAS.items()):
        if not disponibles.get(backend):
            NO_CORRIDO.append("anclas %s/%s: el motor %s no esta en esta maquina"
                              % (backend, modo, backend))
            continue
        obtenidos = []
        for gen in GENES:
            par = leer(gen)
            if par is None:
                NO_CORRIDO.append("anclas %s/%s: falta %s_full.fasta en work/sifi_check"
                                  % (backend, modo, gen))
                obtenidos = None
                break
            _, resumen, _ = api.correr_diseno(par[1], nombre=par[0], modo=modo,
                                              backend=backend)
            obtenidos.append(resumen["eficientes"])
        if obtenidos is None:
            continue
        igual(obtenidos, esperados, "anclas %s/%s sobre %s" % (backend, modo, GENES))


def test_ancla_del_programa_original():
    """Los cuatro conteos que imprimio si-Fi21 con su interfaz, leidos de su propio CSV."""
    disponibles = {m["id"]: m["disponible"] for m in api.motores()}
    if not disponibles.get("exe"):
        NO_CORRIDO.append("ancla del original: hace falta su RNAplfold 2.1.5")
        return

    for gen in GENES:
        # El CSV de ATPaseD quedo con el nombre corto, como lo escribio el programa.
        cands = [W5 / ("sifi21_original_%s.csv" % gen),
                 W5 / ("sifi21_original_%s.csv" % gen.replace("_Dm", ""))]
        ruta = next((c for c in cands if c.is_file()), None)
        if ruta is None:
            NO_CORRIDO.append("ancla del original: no esta el CSV de %s" % gen)
            continue
        with open(ruta, encoding="utf-8") as fh:
            filas = list(csv.DictReader(fh, delimiter=";"))
        if not filas:
            NO_CORRIDO.append("ancla del original: el CSV de %s esta vacio" % gen)
            continue
        del_original = int(filas[0]["Efficient siRNA hits"])

        par = leer(gen)
        if par is None:
            NO_CORRIDO.append("ancla del original: falta el FASTA de %s" % gen)
            continue
        _, resumen, _ = api.correr_diseno(par[1], nombre=par[0], modo="fiel", backend="exe")
        igual(resumen["eficientes"], del_original,
              "%s: el modo fiel reproduce el conteo del programa original" % gen)


def test_curva_del_rnai_design_plot():
    """La curva roja del original: ocho tramos, maximo 9 en 150-156 y 8 en 287-297.

    Es la verificacion del grafico, independiente del total: dos perfiles distintos pueden dar
    el mismo conteo. Se reprodujo tramo por tramo contra la pantalla del programa
    (`research/ola2/W5_secuencias_epilab/sifi21_reproduccion.md`, lineas 85-89).
    """
    disponibles = {m["id"]: m["disponible"] for m in api.motores()}
    if not disponibles.get("exe"):
        NO_CORRIDO.append("curva del design plot: hace falta su RNAplfold 2.1.5")
        return
    par = leer("ATPaseD_Dm")
    if par is None:
        NO_CORRIDO.append("curva del design plot: falta ATPaseD_Dm_full.fasta")
        return

    _, _, c = api.correr_diseno(par[1], nombre=par[0], modo="fiel", backend="exe")
    s = c["solapamiento"]

    tramos = []
    ini = None
    for i, v in enumerate(s, start=1):
        if v > 0 and ini is None:
            ini = i
        elif v == 0 and ini is not None:
            tramos.append((ini, i - 1, max(s[ini - 1:i - 1])))
            ini = None
    if ini is not None:
        tramos.append((ini, len(s), max(s[ini - 1:])))

    igual(len(tramos), 8, "la curva tiene ocho tramos separados")
    igual(max(s), 9, "el maximo de la curva")

    def altura_en(p):
        return next((alt for a, b, alt in tramos if a <= p <= b), None)

    igual(altura_en(150), 9, "el tramo que contiene la posicion 150 mide 9")
    igual(altura_en(156), 9, "el tramo que contiene la posicion 156 mide 9")
    igual(altura_en(287), 8, "el tramo que contiene la posicion 287 mide 8")
    igual(altura_en(297), 8, "el tramo que contiene la posicion 297 mide 8")

    # Las cuatro aserciones de arriba pasan con ancho de cobertura 20 y con 21: miden
    # alturas adentro de un tramo y no sus bordes, asi que no fijan la convencion. Lo que
    # la fija son las dos mesetas exactas y la linea azul, que con 20 caen un nucleotido
    # antes (research/ola5/N2_ancho_de_cobertura/). Sin esto, el dia que alguien cambie el
    # ancho el test sigue en verde y la curva deja de ser la del investigador.
    def meseta(altura):
        tramo, ini = [], None
        for i, v in enumerate(s, start=1):
            if v == altura and ini is None:
                ini = i
            elif v != altura and ini is not None:
                tramo.append((ini, i - 1))
                ini = None
        if ini is not None:
            tramo.append((ini, len(s)))
        return tramo

    igual(meseta(9), [(150, 156)], "la meseta de altura 9 va de 150 a 156")
    igual([t for t in meseta(8) if t[0] == 287], [(287, 297)],
          "la meseta de altura 8 va de 287 a 297")
    igual(max(c["todos"]), 21, "la linea azul queda plana en 21")


# --------------------------------------------------------------- el contrato


def test_contrato_de_curvas():
    """Las dos curvas viven en escalas distintas, y cada una tiene su largo."""
    nombre, seq = leer_ejemplo()
    _, resumen, c = api.correr_diseno(seq, nombre=nombre, modo="corregido")

    igual(len(c["solapamiento"]), c["largo"],
          "la curva de solapamiento tiene un punto por posicion del gen")
    igual(len(c["todos"]), c["largo"], "la curva de referencia tambien")
    igual(len(c["densidad"]), c["n_ventanas"],
          "la curva de densidad tiene un punto por ventana")
    igual(c["n_ventanas"], c["largo"] - c["size"] + 1, "cuantas ventanas entran")
    # La referencia es plana en el tamano de la ventana en todo el interior del gen.
    interior = c["todos"][c["size"]:-c["size"]]
    igual(set(interior), {c["size"]},
          "la referencia de todos los siRNA es plana en %d" % c["size"])
    check(max(c["solapamiento"]) <= c["size"],
          "el solapamiento nunca pasa el tamano de la ventana")
    igual(len(c["eficientes"]), resumen["eficientes"],
          "las posiciones eficientes del contrato son las del resumen")
    check(c["off_perfecto"] is None and c["off_mm1"] is None,
          "sin tamizaje, las tiras de off-target son None y no listas vacias")


def test_densidad_contra_informe_html():
    """`perfil.densidad` da lo mismo que el algoritmo de `informe_html.py:577-585`.

    Son los dos dibujantes del mismo contrato. Si alguien cambia uno, esto falla.
    """
    eficientes = [3, 4, 5, 20, 21, 60, 61, 62, 63, 140]
    n_vent, L = 150, 40

    pre = [0] * (n_vent + 1)
    efic_set = set(eficientes)
    for i in range(1, n_vent + 1):
        pre[i] = pre[i - 1] + (1 if i in efic_set else 0)
    media = (L - 1) // 2
    referencia = []
    for x in range(1, n_vent + 1):
        ini = max(1, x - media)
        fin = min(n_vent, x - media + L - 1)
        referencia.append(pre[fin] - pre[ini - 1])

    igual(perfil.densidad(eficientes, n_vent, L), referencia,
          "la densidad coincide con la de informe_html.py")


def test_solapamiento_de_una_ventana():
    """Una sola ventana eficiente cubre exactamente `size` posiciones."""
    s = perfil.solapamiento([10], largo=100, ancho_cobertura=21)
    igual(sum(1 for v in s if v == 1), 21, "una ventana cubre 21 posiciones")
    igual(s[9], 1, "cubre su propia posicion de arranque")
    igual(s[8], 0, "no cubre la anterior")
    igual(s[29], 1, "cubre hasta 21 nt despues")
    igual(s[30], 0, "y no mas")
    # Contra el borde se recorta y no se sale del array.
    igual(len(perfil.solapamiento([95], largo=100, ancho_cobertura=21)), 100,
          "una ventana contra el borde no desborda")


# --------------------------------------------------------------- parametros


def test_cadena_de_configuracion():
    """La cadena del investigador vuelve igual, y una mal escrita explica que falta."""
    igual(api.cadena_config(api.parsear_config("siFi21_8_1.0_0.1_1111")),
          "siFi21_8_1.0_0.1_1111", "la configuracion declarada por el investigador (D45)")
    p = api.parsear_config("siFi21_8_1.0_0.1_1111")
    igual([p["accessibility_window"], p["end_stability_threshold"],
           p["accessibility_threshold"]], [8, 1.0, 0.1], "los tres numeros")
    igual(all(p[c] for c in api.CASILLAS), True, "las cuatro casillas en verdadero")
    # Los bits son, en el orden del panel: hebra, extremos, accesibilidad, regla terminal.
    # El perfil de off-target del manual (p. 11) deja tildadas la primera y la ultima.
    igual(api.cadena_config(api.PRESETS["diseno"]), "siFi21_8_1.0_0.1_1111",
          "el preset de diseno tilda las cuatro casillas")
    igual(api.cadena_config(api.PRESETS["offtarget"]), "siFi21_8_1.0_0.1_1001",
          "el preset de off-target apaga extremos y accesibilidad")

    for mala in ("", "siFi21_8_1.0_0.1", "nada_8_1.0_0.1_1111", "siFi21_8_1.0_0.1_11",
                 "siFi21_8_1.0_0.1_1112", "siFi21_x_1.0_0.1_1111"):
        try:
            api.parsear_config(mala)
            check(False, "%r tendria que ser rechazada" % mala)
        except ValueError as e:
            check(len(str(e)) > 20, "%r se rechaza con un mensaje que explica" % mala)


def test_validacion_de_parametros():
    """Un parametro fuera de rango se rechaza aca, no dentro de ViennaRNA."""
    casos = [
        ({"sirna_size": 3}, "tamano de siRNA chico"),
        ({"sirna_size": 500}, "tamano de siRNA grande"),
        ({"accessibility_window": 0}, "ventana de accesibilidad en cero"),
        ({"accessibility_window": 99}, "ventana mayor que el siRNA"),
        ({"accessibility_threshold": 1.5}, "umbral de accesibilidad fuera de [0,1]"),
        ({"accessibility_threshold": -0.1}, "umbral de accesibilidad negativo"),
    ]
    for crudo, etq in casos:
        try:
            api.normalizar(crudo)
            check(False, "%s tendria que ser rechazado" % etq)
        except ValueError:
            check(True, "%s se rechaza" % etq)

    p = api.normalizar({})
    igual([p["sirna_size"], p["accessibility_window"]], [21, 8],
          "sin parametros quedan los defaults del original")


def test_modos_son_subconjunto():
    """El corregido es un subconjunto estricto del fiel: ninguna ventana va al revés."""
    par = leer("CP_MRFV")
    if par is None:
        NO_CORRIDO.append("subconjunto de modos: falta CP_MRFV_full.fasta")
        return
    vf, rf, _ = api.correr_diseno(par[1], nombre=par[0], modo="fiel")
    vc, rc, _ = api.correr_diseno(par[1], nombre=par[0], modo="corregido")
    sf = {w.pos for w in vf if w.is_efficient}
    sc = {w.pos for w in vc if w.is_efficient}
    igual(sc - sf, set(), "el corregido no agrega ninguna ventana que el fiel rechace")
    check(len(sf - sc) > 0, "el fiel agrega ventanas por el atajo de la regla terminal")
    check(rf["eficientes"] > rc["eficientes"], "y por eso cuenta mas")


# --------------------------------------------------------------- complejidad


def test_baja_complejidad():
    """El criterio atrapa la cola de poli-A y no toca una secuencia normal."""
    igual(complejidad.es_baja("A" * 21), True, "un 21-mero de poli-A es baja complejidad")
    igual(complejidad.es_baja("C" + "A" * 20), True, "casi todo poli-A tambien")
    igual(complejidad.es_baja("AT" * 10 + "A"), True,
          "dos nucleotidos alternados tambien (<= 2 distintos)")
    igual(complejidad.es_baja("ACGTTGCAAGCTTGACCTAGG"), False,
          "una ventana de composicion normal no")
    igual(complejidad.homopolimero("AACCCGGGGT"), 4, "la racha mas larga")
    igual(complejidad.homopolimero(""), 0, "la racha de la cadena vacia")

    # Un ARNm de RefSeq con composicion normal no tiene casi nada marcado: el criterio no
    # puede estar marcando secuencia comun.
    nombre, seq = leer_ejemplo()
    ventanas, _, _ = api.correr_diseno(seq, nombre=nombre, modo="corregido")
    bajas = complejidad.posiciones_bajas(ventanas)
    check(len(bajas) <= 0.01 * len(ventanas),
          "en el ARNm de maiz del ejemplo se marca casi nada: %d de %d ventanas"
          % (len(bajas), len(ventanas)))

    # El caso real que motivo el criterio: la cola de poli-A del genoma del MRFV, que hace
    # que nueve «coincidencias perfectas de 21/21 nt» en un no objetivo no sean homologia.
    # El archivo vive en work/ y no viaja con la entrega, asi que si no esta, no se corrio.
    mrfv = CHECK / "NC_002786.2.fasta"
    if not mrfv.is_file():
        NO_CORRIDO.append("cola de poli-A del MRFV: falta work/sifi_check/NC_002786.2.fasta")
        return
    nombre, seq = api.leer_fasta(mrfv.read_text(encoding="utf-8"))[0]
    ventanas, _, _ = api.correr_diseno(seq, nombre=nombre, modo="corregido")
    bajas = complejidad.posiciones_bajas(ventanas)
    check(len(bajas) > 0, "el genoma del MRFV tiene ventanas de baja complejidad")
    check(max(bajas) >= len(ventanas) - 2,
          "y estan al final del genoma, que es donde esta la cola de poli-A")
    check(len(bajas) < 0.01 * len(ventanas),
          "son una fraccion chica: %d de %d" % (len(bajas), len(ventanas)))


# --------------------------------------------------------------- rangos


def test_rango_no_guarda_secuencias():
    """Un rango guardado son coordenadas y conteos. La contencion se impone, no se recuerda."""
    guardado = proyecto.guardar({
        "nombre": "prueba de test_api", "gen": "GEN_DE_PRUEBA",
        "inicio": 264, "fin": 563, "eficientes": 199, "modo": "fiel", "motor": "exe",
        # esto no tiene que sobrevivir
        "seq": "ACGTTGCAAGCTTGACCTAGG", "nota": "ACGTACGTACGTACGTACGTACGT",
    })
    check("seq" not in guardado, "la clave seq no se guarda")
    check("nota" not in guardado, "un campo permitido con pinta de secuencia tampoco")
    igual(guardado["largo"], 300, "el largo se calcula")

    texto = (proyecto.CARPETA / guardado["id"]).read_text(encoding="utf-8")
    check("ACGTTGCAAGCTTGACCTAGG" not in texto, "el archivo no contiene la secuencia")
    check(guardado["id"] in {r["id"] for r in proyecto.listar()}, "aparece en el listado")

    invertido = proyecto.guardar({"gen": "G", "inicio": 500, "fin": 100})
    igual([invertido["inicio"], invertido["fin"]], [100, 500],
          "un rango al reves se ordena")

    for r in (guardado["id"], invertido["id"]):
        proyecto.borrar(r)
    check(guardado["id"] not in {x["id"] for x in proyecto.listar()}, "y se puede borrar")

    for falta in ({"inicio": 1, "fin": 2}, {"gen": "G", "fin": 2}, {"gen": "G", "inicio": 1}):
        try:
            proyecto.guardar(falta)
            check(False, "un rango sin %s tendria que ser rechazado" % list(falta))
        except ValueError:
            check(True, "un rango incompleto se rechaza")


def test_tamizaje_contra_dos_bases():
    """Control de cordura del tamizaje: el ejemplo se encuentra a si mismo y nada mas.

    El dato de ejemplo es un ARNm de *Zea mays*, asi que contra el transcriptoma del maiz
    **todas** sus ventanas tienen coincidencia perfecta, y contra un transcriptoma de insecto
    ninguna. Si esos dos numeros dejan de dar eso, el tamizaje esta roto. Es ademas la unica
    cobertura de `offtarget.py`.
    """
    import time

    import offtarget

    disp = {b["id"]: b for b in offtarget.bases_disponibles()}
    maiz = "GCF_902167145.1_Zm-B73-REFERENCE-NAM-5.0_rna"
    bicho = "GCF_914767665.1_icHarAxyr1.1_rna"
    faltan = [b for b in (maiz, bicho) if b not in disp]
    if faltan:
        NO_CORRIDO.append("tamizaje: no estan en work/offtarget_db: %s" % ", ".join(faltan))
        return

    nombre, seq = leer_ejemplo()
    ident = offtarget.lanzar(nombre=nombre, secuencia=seq, bases=[bicho, maiz])
    limite = time.time() + 600
    while time.time() < limite:
        est = offtarget.estado(ident)
        if est["estado"] in ("listo", "error"):
            break
        time.sleep(1)
    else:
        NO_CORRIDO.append("tamizaje: no termino en 10 minutos")
        return

    if est["estado"] == "error":
        check(False, "el tamizaje termino con error: %s" % est["error"])
        return

    r = est["resultado"]
    por_base = {b["base"]: b for b in r["bases"]}
    igual(r["ventanas"], len(seq) - 21 + 1, "una ventana por posicion alcanzable")
    igual(por_base[maiz]["perfecto_21"], r["ventanas"],
          "contra el maiz, el ARNm de maiz se encuentra entero a si mismo")
    igual(por_base[bicho]["perfecto_21"], 0,
          "contra Harmonia axyridis no hay ninguna coincidencia perfecta")
    igual(por_base[bicho]["perfecto_ge19"], 0, "ni un bloque perfecto de 19 nt")
    check(por_base[maiz]["referencias_distintas"] > 0,
          "y el maiz devuelve al menos un registro de referencia")
    # Sin pedir el criterio de un desajuste, la cifra es None y no cero.
    check(por_base[maiz]["mm1_21"] is None and por_base[bicho]["mm1_21"] is None,
          "sin pedirlo, el criterio de un desajuste queda en None y no en cero")
    check(r["off_mm1"] is None, "y la tira del grafico tambien")

    # Una base que no esta en disco se rechaza con su nombre, no con un cero.
    try:
        offtarget.lanzar(nombre="x", secuencia=seq, bases=["no_existe_esta_base"])
        check(False, "una base inexistente tendria que ser rechazada")
    except ValueError as e:
        check("no_existe_esta_base" in str(e), "y el error dice cual falta")
    try:
        offtarget.lanzar(nombre="x", secuencia=seq, bases=[])
        check(False, "tamizar contra ninguna base tendria que ser rechazado")
    except ValueError:
        check(True, "tamizar contra ninguna base se rechaza")


def test_nombres_de_archivo_exportado():
    """Dos exportaciones distintas del mismo gen no pueden caer en el mismo archivo.

    Regresion: `with_suffix` toma todo lo que sigue al ultimo punto como extension, y toda
    accesion del NCBI tiene un punto. `NC_002786.2_ventanas` y `NC_002786.2_features`
    terminaban los dos en `NC_002786.tsv`, uno pisando al otro.
    """
    import exportar

    a = exportar.destino("NC_002786.2_ventanas", ".tsv")
    b = exportar.destino("NC_002786.2_features", ".tsv")
    check(a != b, "dos exportaciones del mismo gen van a archivos distintos")
    igual(a.name, "NC_002786.2_ventanas.tsv", "la accesion sobrevive entera en el nombre")
    igual(exportar.destino("MP_MRFV_full_sirna", ".fasta").name,
          "MP_MRFV_full_sirna.fasta", "un nombre sin puntos tambien")
    igual(exportar.destino("con/barra\\y:dos puntos", ".csv").name,
          "con_barra_y_dos_puntos.csv", "los caracteres de ruta se neutralizan")
    check(exportar.destino("..\\..\\fuera", ".csv").parent == exportar.SALIDAS / "exportado",
          "no se puede escribir fuera de la carpeta de salidas")


def test_lectura_de_fasta():
    """FASTA simple, multiple, con CRLF, y secuencia pelada."""
    igual(api.leer_fasta(">a desc\nACGT\nACGT\n"), [("a", "ACGTACGT")], "FASTA simple")
    igual(api.leer_fasta(">a\nAC\n>b\nGT\n"), [("a", "AC"), ("b", "GT")], "FASTA multiple")
    igual(api.leer_fasta(">a\r\nAC\r\nGT\r\n"), [("a", "ACGT")], "FASTA con CRLF")
    igual(api.leer_fasta("ACGT\nACGT"), [("secuencia_pegada", "ACGTACGT")],
          "secuencia sin encabezado")
    igual(api.leer_fasta("   "), [], "texto vacio no da ninguna secuencia")
    igual(api.leer_fasta(">solo_encabezado\n"), [], "un encabezado sin secuencia no cuenta")


# ------------------------------------------- las vistas de lectura (V1, issue #45)
#
# Que prueban estas verificaciones y que NO prueban. Prueban **lectura y procedencia**: que
# cada vista levante su archivo, que un archivo ausente produzca «no corrido» y no un cero, y
# que ninguna vista escriba fuera del archivo de firmas. No prueban ningun criterio, porque las
# vistas no calculan ninguno: ese es el criterio de terminado de la linea.
#
# Y entran por donde las verificaciones de arriba **no** miran. Las noventa de este archivo
# entran por `api.correr_diseno`, que es el camino del motor; las vistas no lo tocan, asi que
# una vista nueva no puede mover un conteo ancla. Eso no se supone: se verifica leyendo los
# imports de cada modulo de vista.


def _fuente(nombre: str) -> str:
    return (AQUI / nombre).read_text(encoding="utf-8")


VISTAS = ("lectura.py", "vista_region.py", "vista_marcos.py", "vista_juntura.py",
          "vista_ejes.py", "vista_firmas.py", "vista_quimeras.py", "vista_homologia.py")

# Las que SOLO leen. `vista_firmas.py` queda afuera a proposito: es la unica que escribe, y por
# eso es la unica a la que la verificacion de escritura no se le aplica.
VISTAS_DE_LECTURA = ("lectura.py", "vista_region.py", "vista_marcos.py", "vista_juntura.py",
                     "vista_ejes.py", "vista_quimeras.py", "vista_homologia.py")


def test_vistas_no_importan_el_motor():
    """Ninguna vista importa `api` ni nada de `tools/sifi21_port/`. Leido, no supuesto.

    Es la garantia de que las vistas no pueden mover un numero: no llaman al motor. Se mira el
    arbol sintactico y no una expresion regular, porque `import api` adentro de un comentario o
    de una cadena no es un import y un grep no sabe la diferencia.
    """
    import ast

    prohibidos = {"api", "sifi_pipeline", "sifi_core", "ranking", "ranking_v2", "alertas",
                  "offtarget_21nt", "identidad", "ejes_separados", "conservacion"}
    for nombre in VISTAS:
        arbol = ast.parse(_fuente(nombre), filename=nombre)
        importados = set()
        for nodo in ast.walk(arbol):
            if isinstance(nodo, ast.Import):
                importados |= {a.name.split(".")[0] for a in nodo.names}
            elif isinstance(nodo, ast.ImportFrom) and nodo.module:
                importados.add(nodo.module.split(".")[0])
        igual(sorted(importados & prohibidos), [],
              "%s no importa el motor ni el port" % nombre)


def test_vistas_leen_su_archivo():
    """Cada vista levanta su archivo y devuelve las filas que el archivo tiene.

    Las cifras se comparan contra el conteo de filas del archivo en disco, no contra un numero
    escrito aca: lo que se verifica es que la vista no pierda ni invente filas, no cuantas filas
    tiene hoy el archivo.
    """
    import csv as _csv

    import vista_ejes
    import vista_firmas
    import vista_juntura
    import vista_marcos
    import vista_region

    def filas_de(ruta):
        with open(ruta, encoding="utf-8", newline="") as fh:
            return [f for f in _csv.DictReader(fh, delimiter="\t")
                    if any((v or "").strip() for v in f.values())]

    # Vista A: el inventario de regiones son los archivos que hay en el directorio.
    inv = vista_region.inventario()
    if inv["estado"] != "listo":
        NO_CORRIDO.append("vista A: %s" % inv.get("motivo"))
    else:
        igual(len(inv["regiones"]), len(list(vista_region.POR_REGION.glob("*.tsv"))),
              "la vista A lista todas las regiones del directorio")
        # El nombre se parte por el ultimo guion bajo: los genes tienen guiones adentro.
        claves = {r["clave"]: r for r in inv["regiones"]}
        if "ATPaseD_Dm_137-436" in claves:
            igual([claves["ATPaseD_Dm_137-436"]["gen"],
                   claves["ATPaseD_Dm_137-436"]["region"]], ["ATPaseD_Dm", "137-436"],
                  "un gen con guion bajo en el nombre se parte bien")

    v = vista_region.ver("BicC_Dm_264-563", "BicC_Dm_922-1221")
    if v["estado"] != "listo":
        NO_CORRIDO.append("vista A: %s" % v.get("motivo"))
    else:
        a, b = v["paneles"]
        igual([a["n_filas"], b["n_filas"]],
              [len(filas_de(vista_region.POR_REGION / "BicC_Dm_264-563.tsv")),
               len(filas_de(vista_region.POR_REGION / "BicC_Dm_922-1221.tsv"))],
              "la vista A devuelve las filas que tienen los dos archivos")
        check(not a["contradicciones"] and not b["contradicciones"],
              "las dos cifras del mismo hecho coinciden entre los dos archivos de M6")
        # La unidad de conteo es la posicion y no la fila: las isoformas del mismo gen son
        # varias filas de la tabla por ventana para una sola posicion.
        por_org = {m["organismo_corto"]: m for m in a["marcas"] if m["criterio"] == "perfecto_21"}
        if "H_vitripennis" in por_org:
            igual(por_org["H_vitripennis"]["posiciones"],
                  por_org["H_vitripennis"]["filas_del_archivo"],
                  "las posiciones con 21/21 coinciden con lo que declara la tabla por region")
        igual(v["procedencia"]["panel"], lectura.NO_DECLARADA,
              "el panel de M6 no esta declarado y la vista A lo dice")
        igual([v["procedencia"]["modo"], v["procedencia"]["motor"]],
              [lectura.NO_APLICA, lectura.NO_APLICA],
              "un conteo de coincidencias exactas no depende del modo ni del motor")

    # Vista B: una fila por region, y la cabecera es la del marco 3.
    m = vista_marcos.ver()
    if m["estado"] != "listo":
        NO_CORRIDO.append("vista B: %s" % m.get("motivo"))
    else:
        igual(len(m["regiones"]), len(filas_de(vista_marcos.TSV)),
              "la vista B devuelve las regiones que tiene el archivo")
        igual([r["cabecera"]["marco"] for r in m["regiones"]], [3] * len(m["regiones"]),
              "la cifra de cabecera de cada region es la del marco 3")
        for r in m["regiones"]:
            igual(r["cabecera"]["valor"],
                  next(c["valor"] for c in r["cifras"] if c["marco"] == 3),
                  "y es la misma cifra que la del marco 3 en la lista (%s)" % r["gen"])
        igual(len(m["regiones"][0]["cifras"]), 3, "las tres cifras van las tres")
        check(m["procedencia"]["declarada"],
              "la vista B declara su procedencia: %s / %s" % (m["procedencia"]["modo"],
                                                             m["procedencia"]["motor"]))

    # Vista C: los bloques del detalle, contrastados con el resumen de la misma corrida.
    j = vista_juntura.ver()
    if j["estado"] != "listo":
        NO_CORRIDO.append("vista C: %s" % j.get("motivo"))
    else:
        igual(len(j["ordenes"]), len(filas_de(vista_juntura.RESUMEN)),
              "la vista C devuelve los ordenes que tiene el resumen")
        igual(j["contradicciones"], [],
              "el detalle y el resumen de la juntura coinciden en los dos conteos")
        for o in j["ordenes"]:
            igual(o["fabricados"], o["resumen"]["bloques_fabricados_por_el_empalme"],
                  "%s: los bloques fabricados del dibujo son los del resumen" % o["quimera"])
            igual(o["heredados"] + o["fabricados"], o["resumen"]["bloques_con_acierto"],
                  "%s: heredados mas fabricados son los bloques con acierto" % o["quimera"])
        # Lo que el archivo NO trae se declara como no medido, con las dos cifras y su fuente.
        c = j["cobertura_de_bloques"]
        igual(c["en_el_archivo"] + c["no_medidos"], c["publicados"],
              "los bloques del archivo mas los no medidos son los publicados")
        check(c["en_el_archivo"] < c["publicados"],
              "el detalle trae %d de los %d bloques publicados, y la vista lo declara"
              % (c["en_el_archivo"], c["publicados"]))

    # Vista E: las dos columnas que dependen del panel van sin procedencia.
    e = vista_ejes.ver()
    if e["estado"] != "listo":
        NO_CORRIDO.append("vista E: %s" % e.get("motivo"))
    else:
        igual(len(e["objetos"]), len(filas_de(vista_ejes.TSV)),
              "la vista E devuelve los objetos que tiene el archivo")
        igual(e["procedencia"]["panel"], lectura.NO_DECLARADA,
              "el panel de los ejes no esta declarado y la vista E lo dice")
        for o in e["objetos"]:
            igual(o["limpieza"]["procedencia"], lectura.NO_DECLARADA,
                  "la limpieza de %s depende del panel y va sin procedencia" % o["objeto"])

    # Vista D: el contador de pendientes es el del inventario.
    f = vista_firmas.ver()
    if f["estado"] != "listo":
        NO_CORRIDO.append("vista D: %s" % f.get("motivo"))
    else:
        filas = filas_de(vista_firmas.INVENTARIO)
        igual(f["total"], len(filas), "la bandeja devuelve las filas del inventario")
        igual(f["pendientes"],
              sum(1 for x in filas if (x.get("decision_usuario") or "").strip() == "pendiente"),
              "el contador de pendientes coincide con las filas en «pendiente»")
        igual(sum(f["cuenta"].values()), len(filas),
              "cada fila esta en exactamente un estado")
        # Los cuatro campos obligatorios de D48, completos en cada ficha.
        for x in f["filas"]:
            igual(sorted(x["campos"]), sorted(vista_firmas.CAMPOS_OBLIGATORIOS),
                  "la ficha de %s trae los cuatro campos de D48" % x["clave"])
            break
        vacios = [x["clave"] for x in f["filas"]
                  for campo, cols in x["campos"].items()
                  for c, v in cols.items() if not str(v).strip()]
        igual(vacios, [], "ninguna ficha tiene un campo obligatorio vacio")


def test_una_vista_sin_su_archivo_dice_no_corrido():
    """Un insumo que no esta produce «no corrido» y **no** un cero.

    Se apunta cada modulo a una ruta que no existe en vez de renombrar el archivo de verdad:
    renombrar un resultado de otra linea para correr una prueba es la clase de cosa que queda
    renombrada. El efecto sobre el codigo de la vista es el mismo.
    """
    import vista_ejes
    import vista_firmas
    import vista_homologia
    import vista_juntura
    import vista_marcos
    import vista_region

    falso = AQUI / "no_existe_este_archivo_de_prueba.tsv"
    casos = [
        (vista_region, "POR_VENTANA", lambda: vista_region.ver("BicC_Dm_264-563",
                                                               "BicC_Dm_922-1221")),
        (vista_marcos, "TSV", vista_marcos.ver),
        (vista_juntura, "RESUMEN", vista_juntura.ver),
        (vista_ejes, "TSV", vista_ejes.ver),
        (vista_firmas, "INVENTARIO", vista_firmas.ver),
        (vista_homologia, "RESUMEN_LECTURA", vista_homologia.ver),
    ]
    for modulo, atributo, llamar in casos:
        original = getattr(modulo, atributo)
        try:
            setattr(modulo, atributo, falso)
            d = llamar()
        finally:
            setattr(modulo, atributo, original)
        igual(d.get("estado"), "no corrido",
              "%s sin su archivo declara «no corrido»" % modulo.__name__)
        check(falso.name in d.get("archivo", ""),
              "%s dice cual es el archivo que falta" % modulo.__name__)
        # Lo que importa: ni una sola cifra en la respuesta. Un cero aca se leeria como «se
        # miro y no hay nada», que es justo lo contrario de lo que paso.
        numeros = [k for k, v in d.items() if isinstance(v, (int, float))
                   and not isinstance(v, bool)]
        igual(numeros, [], "%s no devuelve ningun numero cuando falta el archivo"
              % modulo.__name__)


def test_la_vista_de_marcos_sin_su_configuracion():
    """Falta el JSON de configuracion: las cifras salen con «procedencia no declarada».

    Es el caso intermedio y el mas facil de hacer mal: el TSV esta, asi que hay cifras, pero el
    unico archivo que dice con que modo y que motor se contaron no esta. Adivinarlo del nombre
    del archivo seria exactamente lo que el preregistro prohibe.
    """
    import vista_marcos

    original = vista_marcos.JSON
    try:
        vista_marcos.JSON = AQUI / "no_existe_esta_configuracion.json"
        d = vista_marcos.ver()
    finally:
        vista_marcos.JSON = original

    igual(d["estado"], "listo", "con el TSV presente la vista igual muestra las cifras")
    igual(d["configuracion_declarada"], False, "pero declara que la configuracion no esta")
    igual([d["procedencia"]["modo"], d["procedencia"]["motor"]],
          [lectura.NO_DECLARADA, lectura.NO_DECLARADA],
          "y el modo y el motor salen como «procedencia no declarada»")
    check(d["regiones"][0]["cabecera"]["valor"] is not None,
          "la cifra sigue estando: lo que falta es su procedencia, no el numero")


def test_las_constantes_de_firma_no_se_separaron_del_motor():
    """El tripwire: las reglas de D48 de la vista son las mismas que las del motor.

    La vista no puede importar `tools/sifi21_port/alertas.py` —la linea no toca el motor— asi
    que las constantes estan duplicadas. Duplicadas sin red es como las dos copias se separan
    en silencio. El archivo del motor se lee como **texto** y se parsea su arbol sintactico: ni
    se importa ni se ejecuta, que es lo que mantiene la frontera.
    """
    import ast

    import vista_firmas

    ruta = api.RAIZ / "tools" / "sifi21_port" / "alertas.py"
    if not ruta.is_file():
        NO_CORRIDO.append("tripwire de firmas: no esta %s" % ruta)
        return

    arbol = ast.parse(ruta.read_text(encoding="utf-8"), filename=str(ruta))
    delmotor = {}
    for nodo in arbol.body:
        if isinstance(nodo, ast.Assign) and isinstance(nodo.targets[0], ast.Name):
            try:
                delmotor[nodo.targets[0].id] = ast.literal_eval(nodo.value)
            except ValueError:
                pass

    igual(vista_firmas.DECISIONES, delmotor.get("DECISIONES"),
          "el vocabulario de decisiones de la vista es el del motor")
    igual(vista_firmas.MARCA_PENDIENTE, delmotor.get("MARCA_PENDIENTE"),
          "la marca de pendiente es la del motor")
    igual(vista_firmas.PROSA_MINIMA, delmotor.get("PROSA_MINIMA"),
          "el minimo de prosa de D48 es el del motor")
    igual(vista_firmas.COLUMNAS_DECISION, delmotor.get("COLUMNAS_DECISION"),
          "el esquema del archivo de firmas es el del motor")
    igual(sorted(vista_firmas.CAMPOS_OBLIGATORIOS),
          sorted(delmotor.get("CAMPOS_OBLIGATORIOS", ())),
          "los cuatro campos obligatorios son los del motor")
    # Y las columnas que materializan cada campo, que es donde mas facil se separan.
    igual({k: tuple(v) for k, v in vista_firmas.CAMPOS_OBLIGATORIOS.items()},
          {k: tuple(v) for k, v in (delmotor.get("COLUMNAS_DE") or {}).items()},
          "y las columnas de cada campo tambien")


def test_una_firma_sin_justificacion_se_rechaza():
    """Las cinco formas de rechazar una firma, y el inventario sin tocar.

    La escritura se prueba contra una **copia** del archivo de firmas: esta linea construye la
    bandeja y no firma ninguna alerta, asi que una prueba que dejara una firma de verdad en
    `decisiones.tsv` estaria firmando en nombre del equipo.
    """
    import hashlib
    import shutil
    import tempfile

    import vista_firmas

    def huella_del_inventario():
        return hashlib.sha256(vista_firmas.INVENTARIO.read_bytes()).hexdigest()

    antes = huella_del_inventario()
    filas, _ = lectura.leer_tsv(vista_firmas.INVENTARIO)
    pendientes = [f for f in filas
                  if (f.get("decision_usuario") or "").strip() == "pendiente"]
    if not pendientes:
        NO_CORRIDO.append("firmas: no hay ninguna fila en «pendiente» para probar")
        return
    fila = pendientes[0]
    clave = "|".join(str(x) for x in vista_firmas.clave_de(fila))
    locus = (fila.get("gen_locus") or "").strip()
    buena = ("Justificacion de prueba, larga y que cita la fila por su locus %s, escrita "
             "solo para verificar el camino de escritura." % locus)

    malas = [
        ("aceptada", "corto", "una justificacion de una palabra"),
        ("aceptada", "pendiente: " + "x" * 80 + " " + locus, "el texto de relleno"),
        ("aceptada", "Un parrafo largo que no nombra el locus ni ninguna accesion de la fila, "
                     "pero pasa el minimo de caracteres sin ningun problema.",
         "una justificacion que no cita la fila"),
        ("pendiente", buena, "una firma que dice «pendiente»"),
        ("tal vez", buena, "una decision fuera del vocabulario"),
    ]
    for decision, texto, que in malas:
        try:
            vista_firmas.firmar(clave, decision, texto, firmado_por="test_api")
            check(False, "%s tendria que ser rechazada" % que)
        except vista_firmas.FirmaRechazada as e:
            check(len(str(e)) > 40, "%s se rechaza con un mensaje que explica" % que)

    # Sin autor tampoco, que es la quinta.
    try:
        vista_firmas.firmar(clave, "aceptada", buena, firmado_por="  ")
        check(False, "una firma sin autor tendria que ser rechazada")
    except vista_firmas.FirmaRechazada:
        check(True, "una firma sin autor se rechaza")

    igual(huella_del_inventario(), antes,
          "ninguna firma rechazada toco el inventario de alertas")

    # Y ahora el camino que si escribe, contra una copia.
    original = vista_firmas.FIRMAS
    carpeta = tempfile.mkdtemp(prefix="sifi_firmas_")
    copia = Path(carpeta) / "decisiones.tsv"
    try:
        if original.is_file():
            shutil.copy2(original, copia)
        firmas_antes = len(lectura.leer_tsv(copia)[0]) if copia.is_file() else 0
        vista_firmas.FIRMAS = copia
        r = vista_firmas.firmar(clave, "aceptada", buena, firmado_por="test_api")

        igual(r["escrito"], True, "una firma bien escrita se escribe")
        igual(r["reemplazada"], False, "y es nueva, no un reemplazo")
        escritas, _ = lectura.leer_tsv(copia)
        igual(len(escritas), firmas_antes + 1, "el archivo de firmas gana exactamente una fila")

        nueva = next(f for f in escritas
                     if "|".join(str(x) for x in vista_firmas.clave_de(f)) == clave)
        # La huella se lee de la fila, no de lo que mande quien firma: es lo unico que ata la
        # firma a la fila que el firmante tenia delante.
        igual([nueva["huella_21"], nueva["huella_ge19"]],
              [str(fila["ventanas_perfecto_21"]).strip(),
               str(fila["ventanas_perfecto_ge19"]).strip()],
              "la huella de la firma es la de la fila del inventario")
        igual(nueva["firmado_por"], "test_api", "la firma guarda quien firmo")
        check(len(nueva["fecha"]) == 10 and nueva["fecha"][4] == "-",
              "y cuando, en formato de fecha")
        igual(sorted(nueva), sorted(vista_firmas.COLUMNAS_DECISION),
              "el archivo de firmas tiene las diez columnas del esquema y ninguna mas")

        # Firmar de nuevo la misma clave reemplaza, no duplica: dos firmas para la misma fila
        # son un error que el generador levanta.
        r2 = vista_firmas.firmar(clave, "bloqueante", buena, firmado_por="test_api")
        igual(r2["reemplazada"], True, "volver a firmar la misma fila reemplaza la firma")
        igual(len(lectura.leer_tsv(copia)[0]), firmas_antes + 1,
              "y no deja dos firmas para la misma fila")

        igual(huella_del_inventario(), antes,
              "escribir una firma no modifica el inventario de alertas")
        check(not original.is_file() or
              hashlib.sha256(original.read_bytes()).hexdigest() !=
              hashlib.sha256(copia.read_bytes()).hexdigest(),
              "y la escritura fue a la copia, no al archivo de firmas del repositorio")
    finally:
        vista_firmas.FIRMAS = original
        shutil.rmtree(carpeta, ignore_errors=True)


def test_ninguna_vista_escribe_fuera_del_archivo_de_firmas():
    """Las cuatro vistas de lectura no escriben en ningun lado, y la quinta en un solo lugar.

    Se verifica de dos formas, porque ninguna sola alcanza: leyendo el arbol sintactico de cada
    modulo —ninguna llamada de escritura fuera de `vista_firmas`— y corriendo las cuatro vistas
    con el arbol del repositorio vigilado por huella.
    """
    import ast
    import hashlib

    import vista_ejes
    import vista_homologia
    import vista_juntura
    import vista_marcos
    import vista_quimeras
    import vista_region

    # 1. Estatico: que no haya una sola llamada de escritura en las vistas de lectura.
    escritura = {"write_text", "write_bytes", "mkdir", "unlink", "replace", "rename",
                 "mkstemp", "rmtree", "remove"}
    for nombre in VISTAS_DE_LECTURA:
        arbol = ast.parse(_fuente(nombre), filename=nombre)
        usos = set()
        for nodo in ast.walk(arbol):
            if isinstance(nodo, ast.Call):
                f = nodo.func
                if isinstance(f, ast.Attribute) and f.attr in escritura:
                    usos.add(f.attr)
                if isinstance(f, ast.Name) and f.id == "open":
                    modos = [a.value for a in nodo.args[1:2]
                             if isinstance(a, ast.Constant)]
                    modos += [k.value.value for k in nodo.keywords
                              if k.arg == "mode" and isinstance(k.value, ast.Constant)]
                    if any("w" in str(m) or "a" in str(m) for m in modos):
                        usos.add("open en modo escritura")
                if isinstance(f, ast.Attribute) and f.attr == "open":
                    modos = [a.value for a in nodo.args[:1] if isinstance(a, ast.Constant)]
                    modos += [k.value.value for k in nodo.keywords
                              if k.arg == "mode" and isinstance(k.value, ast.Constant)]
                    if any("w" in str(m) or "a" in str(m) for m in modos):
                        usos.add("Path.open en modo escritura")
        igual(sorted(usos), [], "%s no tiene ninguna llamada de escritura" % nombre)

    # 2. Dinamico: correr las cuatro vistas y verificar que el arbol no cambio.
    vigilados = [vista_region.POR_VENTANA, vista_marcos.TSV, vista_marcos.JSON,
                 vista_juntura.RESUMEN, vista_juntura.DETALLE, vista_juntura.CAMBIADAS,
                 vista_ejes.TSV, vista_region.POR_REGION / "BicC_Dm_264-563.tsv",
                 vista_quimeras._rutas("eficiencia_heredada")[0],
                 vista_quimeras._rutas("eficiencia_heredada")[1],
                 vista_homologia.RESUMEN_LECTURA, vista_homologia.RESUMEN,
                 vista_homologia.CONTROLES,
                 vista_homologia.F1 / "transferencia_HV.tsv.gz"]
    huellas = {p: hashlib.sha256(p.read_bytes()).hexdigest()
               for p in vigilados if p.is_file()}
    vista_region.ver("BicC_Dm_264-563", "BicC_Dm_922-1221")
    vista_marcos.ver()
    vista_juntura.ver()
    vista_ejes.ver()
    if vista_quimeras._rutas("eficiencia_heredada")[0].is_file():
        vista_quimeras.ver("eficiencia_heredada", cuantas=5)
    if vista_homologia.RESUMEN_LECTURA.is_file():
        vista_homologia.ver("HV")
        vista_homologia.detalle("HV", "f_reciproco_con_nombre", cuantas=5)
    for p, h in huellas.items():
        igual(hashlib.sha256(p.read_bytes()).hexdigest(), h,
              "leer las vistas no modifico %s" % p.name)


def test_las_quimeras_no_se_reordenan():
    """El orden de la tabla es el del archivo, y el filtro no renumera (V2).

    Es la forma de romper la regla de la linea que esta vista trae y las cinco de V1 no: los tres
    objetivos son **las mismas quimeras ordenadas distinto**, asi que el primer puesto es la
    respuesta de ese objetivo. Si la vista reordenara por una columna propia, estaria calculando
    un criterio nuevo y presentandolo como el de O4.
    """
    import csv as _csv

    import vista_quimeras

    primeras, conjuntos = {}, {}
    for objetivo in vista_quimeras.OBJETIVOS:
        tsv, _ = vista_quimeras._rutas(objetivo)
        if not tsv.is_file():
            NO_CORRIDO.append("quimeras: no esta %s" % lectura.rel(tsv))
            continue
        d = vista_quimeras.ver(objetivo, cuantas=5)
        igual(d["estado"], "listo", "el objetivo %s se lee" % objetivo)

        with tsv.open(encoding="utf-8", newline="") as fh:
            crudas = [f for f in _csv.DictReader(fh, delimiter="\t")
                      if (f.get("quimera") or "").strip()]
        igual(d["total_en_el_archivo"], len(crudas),
              "%s: la vista devuelve las filas del archivo" % objetivo)
        # El orden, fila por fila, es el del archivo.
        igual([f["quimera"] for f in d["filas"]],
              [f["quimera"] for f in crudas[:5]],
              "%s: las primeras cinco salen en el orden del archivo" % objetivo)
        igual([f["puesto_en_el_archivo"] for f in d["filas"]], [1, 2, 3, 4, 5],
              "%s: el puesto es la posicion en el archivo" % objetivo)
        primeras[objetivo] = crudas[0]["quimera"]
        conjuntos[objetivo] = {f["quimera"] for f in crudas}

    if len(conjuntos) > 1:
        # Las mismas quimeras en los tres, y al menos dos primeros puestos distintos: eso es lo
        # que hace que el orden sea el criterio y no una propiedad de la quimera.
        valores = list(conjuntos.values())
        check(all(v == valores[0] for v in valores),
              "los tres objetivos traen exactamente las mismas quimeras")
        check(len(set(primeras.values())) > 1,
              "y el primer puesto cambia segun el objetivo: %s"
              % ", ".join("%s=%s" % (k, v.split("__")[0]) for k, v in primeras.items()))

    # El filtro recorta y NO renumera: si renumerara, el filtro seria un criterio.
    if "eficiencia_heredada" in conjuntos:
        f = vista_quimeras.ver("eficiencia_heredada", solo_con_alerta=True, cuantas=10)
        if f["total_filtrado"]:
            puestos = [x["puesto_en_el_archivo"] for x in f["filas"]]
            igual(puestos, sorted(puestos), "el filtro conserva el orden del archivo")
            check(puestos != list(range(1, len(puestos) + 1)) or f["total_filtrado"] ==
                  f["total_en_el_archivo"],
                  "y conserva el puesto original en vez de renumerar desde 1 (%s)"
                  % puestos[:5])
            check(all((x["alerta_juntura_nueva"] or "").strip() == "si" for x in f["filas"]),
                  "el filtro de alerta devuelve solo las que la tienen")
        # Un objetivo que no existe se rechaza con los que si.
        try:
            vista_quimeras.ver("no_existe_este_objetivo")
            check(False, "un objetivo inexistente tendria que ser rechazado")
        except ValueError as e:
            check("eficiencia_heredada" in str(e),
                  "y el error dice cuales son los objetivos validos")
        # La advertencia del archivo viaja con la tabla.
        d = vista_quimeras.ver("eficiencia_heredada", cuantas=1)
        check(len(d["advertencia"]) > 40,
              "la advertencia del archivo viaja con la tabla y no se pierde")
        check(d["grilla"]["combinaciones_antes_de_podar"] >
              d["grilla"]["combinaciones_admisibles"],
              "la grilla declara cuanto podo: %s a %s"
              % (d["grilla"]["combinaciones_antes_de_podar"],
                 d["grilla"]["combinaciones_admisibles"]))


def test_la_homologia_distingue_lo_preregistrado_de_lo_post_hoc():
    """La cifra de cabecera es la variante preregistrada, no la que rinde mas (V2).

    La ampliada se definio despues de ver los datos y da mas del doble de ORFs reciprocos.
    Mostrarla de cabecera porque es mas grande seria elegir el numero despues de verlo, que es
    lo que un preregistro existe para impedir.
    """
    import vista_homologia

    if not vista_homologia.RESUMEN_LECTURA.is_file():
        NO_CORRIDO.append("homologia: no esta %s"
                          % lectura.rel(vista_homologia.RESUMEN_LECTURA))
        return

    d = vista_homologia.ver("HV")
    igual(d["estado"], "listo", "la vista de homologia se lee")

    cabecera = [v for v in d["variantes"] if v["es_la_de_cabecera"]]
    igual(len(cabecera), 1, "hay exactamente una variante de cabecera")
    igual(cabecera[0]["variante"], "estricta_preregistrada",
          "y la de cabecera es la preregistrada")
    igual(cabecera[0]["rotulo"], "preregistrada", "rotulada como tal")

    post = next(v for v in d["variantes"] if v["variante"] == "ampliada_H_post_hoc")
    igual(post["rotulo"], "post hoc", "y la otra queda rotulada post hoc")
    # El punto entero: la post hoc rinde MAS y aun asi no es la de cabecera.
    check(post["orfs_reciprocos"] > cabecera[0]["orfs_reciprocos"],
          "la post hoc rinde mas ORF reciprocos (%s contra %s) y aun asi no es la de cabecera"
          % (post["orfs_reciprocos"], cabecera[0]["orfs_reciprocos"]))

    # El control positivo va junto a la cifra, con su veredicto tal como el archivo lo trae.
    c = d["controles"]["positivo"]
    check(c["pasa_estricta"] is not None,
          "el control positivo declara si pasa la variante estricta")
    check(len(c["lectura"]) > 40, "y viene con su lectura, no suelto")
    sen = d["controles"]["senuelo"]["por_referencia"]
    check(bool(sen), "el senuelo se muestra")

    # La procedencia de esta vista no lleva modo ni motor, y lo dice.
    igual([d["procedencia"]["modo"], d["procedencia"]["motor"]],
          [lectura.NO_APLICA, lectura.NO_APLICA],
          "una transferencia por homologia no pasa por el criterio de si-Fi: no aplica")
    check(len(d["referencias_con_huella"]) >= 1,
          "y el lugar del panel lo ocupan las referencias con su huella")

    # El embudo cierra contra el resumen: la categoria final es «con nombre informativo».
    if d["embudo"]:
        con_nombre = next(e["n"] for e in d["embudo"]
                          if e["categoria"] == "f_reciproco_con_nombre")
        igual(con_nombre, cabecera[0]["con_nombre_informativo"],
              "la ultima categoria del embudo es la cifra de ORF con nombre del resumen")
        reciprocos = con_nombre + next(e["n"] for e in d["embudo"]
                                       if e["categoria"] == "e_reciproco_sin_nombre")
        igual(reciprocos, cabecera[0]["orfs_reciprocos"],
              "y las dos categorias reciprocas suman los ORF reciprocos")

    # El detalle se pagina: 131.683 filas no se vuelcan enteras.
    det = vista_homologia.detalle("HV", "f_reciproco_con_nombre", cuantas=10)
    igual(det["estado"], "listo", "el detalle se lee")
    check(len(det["filas"]) <= 10, "y respeta el tope de filas pedido")
    check(det["total_del_archivo"] > len(det["filas"]),
          "el archivo tiene %s filas y la pagina trae %s"
          % (det["total_del_archivo"], len(det["filas"])))
    igual(det["total"], con_nombre if d["embudo"] else det["total"],
          "el total filtrado por categoria es el del embudo")
    # Un tope absurdo se recorta en vez de volcar el archivo entero.
    grande = vista_homologia.detalle("HV", "f_reciproco_con_nombre", cuantas=99999)
    check(len(grande["filas"]) <= 500,
          "un tope absurdo se recorta a 500 y no vuelca el archivo entero")

    for malo, que in (("no_existe", "una referencia inexistente"),):
        try:
            vista_homologia.ver(malo)
            check(False, "%s tendria que ser rechazada" % que)
        except ValueError:
            check(True, "%s se rechaza" % que)
    try:
        vista_homologia.detalle("HV", "no_es_una_categoria")
        check(False, "una categoria inexistente tendria que ser rechazada")
    except ValueError as e:
        check("f_reciproco_con_nombre" in str(e), "y el error lista las categorias validas")

    # La v1 descartada no se lee ni se muestra como resultado.
    check("DESCARTADA" in d["descartado"]["estado"],
          "la v1 descartada se nombra como descartada y no como resultado")


def test_las_pestanas_apagadas_siguen_construidas_y_ruteadas():
    """Las siete vistas estan escondidas en la interfaz y enteras por debajo.

    Esconder una pestana es apagar su boton, no desconectar la vista. Lo que esta verificacion
    cuida es que las dos cosas no se confundan: que la lista de apagadas nombre pestanas que
    **existen** —una entrada con un nombre viejo apagaria nada y nadie se enteraria— y que cada
    vista apagada siga teniendo su seccion, su ruta y su modulo. El dia que alguien vuelva a
    prender una, tiene que encontrarla funcionando.
    """
    import re

    js = (AQUI / "estatico" / "app.js").read_text(encoding="utf-8")
    html = (AQUI / "estatico" / "index.html").read_text(encoding="utf-8")
    servidor = _fuente("servidor.py")

    m = re.search(r"const VISTAS_OCULTAS = \[(.*?)\];", js, re.S)
    if m is None:
        check(False, "no encontre la lista VISTAS_OCULTAS en app.js")
        return
    ocultas = re.findall(r"'([a-z]+)'", m.group(1))
    igual(len(ocultas), len(set(ocultas)), "la lista de apagadas no repite ninguna")

    # Toda pestana apagada tiene que existir: boton, seccion y cargador.
    botones = set(re.findall(r'data-vista="([a-z]+)"', html))
    for v in ocultas:
        check(v in botones, "la pestana apagada %r existe en el HTML" % v)
        check('id="vista-%s"' % v in html, "y la seccion de %r sigue en el HTML" % v)
    # Y ninguna de las tres originales esta apagada: apagar «diseno» dejaria la demo sin nada.
    for v in ("diseno", "off", "rangos"):
        check(v not in ocultas, "la pestana original %r sigue visible" % v)

    # Las vistas de V1 y V2 estan todas apagadas hoy. Si alguna se prende, esta verificacion
    # falla y hay que decidirlo a proposito en vez de que pase por un descuido.
    esperadas = {"regionv", "marcos", "juntura", "ejes", "quimeras", "homologia", "firmas"}
    igual(set(ocultas), esperadas,
          "las siete vistas de V1 y V2 estan apagadas en la interfaz")

    # Lo que NO se apago: las rutas siguen ruteadas y los modulos siguen importados, que es la
    # diferencia entre «escondida» y «desconectada».
    for ruta in ("/api/vista/region", "/api/vista/marcos", "/api/vista/juntura",
                 "/api/vista/ejes", "/api/vista/firmas", "/api/vista/quimeras",
                 "/api/vista/homologia"):
        check(ruta in servidor, "la ruta %s sigue ruteada con la pestana apagada" % ruta)
    for modulo in ("vista_region", "vista_marcos", "vista_juntura", "vista_ejes",
                   "vista_firmas", "vista_quimeras", "vista_homologia"):
        check(re.search(r"^import %s$" % modulo, servidor, re.M) is not None,
              "el servidor sigue importando %s" % modulo)


def test_el_servidor_sigue_atado_a_localhost():
    """El socket se ata a `127.0.0.1` y a ninguna interfaz de red.

    Es la regla de confidencialidad del proyecto y no una promesa en un documento: si alguien
    cambia esa linea, cambia la garantia. Las vistas nuevas no la tocan, y esto lo verifica.
    """
    import ast

    fuente = _fuente("servidor.py")
    arbol = ast.parse(fuente, filename="servidor.py")
    direcciones = set()
    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.Tuple) and nodo.elts:
            primero = nodo.elts[0]
            if isinstance(primero, ast.Constant) and isinstance(primero.value, str):
                if primero.value.count(".") == 3 or primero.value in ("", "localhost"):
                    direcciones.add(primero.value)
    igual(sorted(direcciones), ["127.0.0.1"],
          "el servidor se ata solo a 127.0.0.1")

    # `0.0.0.0` **si** aparece en el servidor, en la prosa que explica por que no se usa, y esa
    # frase es parte de la garantia: dice cual es la decision y que pasa si alguien la cambia.
    # Lo que no puede existir es una cadena `0.0.0.0` en el codigo. Se separan las dos cosas
    # sacando los docstrings del arbol, que es la diferencia entre documentar una decision y
    # tomarla al reves.
    docs = set()
    for nodo in ast.walk(arbol):
        if isinstance(nodo, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            d = ast.get_docstring(nodo, clean=False)
            if d is not None:
                docs.add(d)
    cadenas = [n.value for n in ast.walk(arbol)
               if isinstance(n, ast.Constant) and isinstance(n.value, str)
               and n.value not in docs]
    check(not any("0.0.0.0" in s for s in cadenas),
          "no hay ninguna cadena 0.0.0.0 en el codigo del servidor")
    check("0.0.0.0" in fuente,
          "y la prosa sigue explicando por que no se ata a 0.0.0.0")

    # Las rutas de las vistas estan ruteadas, que es lo que hace que la verificacion de arriba
    # sea sobre el servidor que de verdad las sirve.
    for ruta in ("/api/vista/region", "/api/vista/marcos", "/api/vista/juntura",
                 "/api/vista/ejes", "/api/vista/firmas", "/api/vista/firmar",
                 "/api/vista/quimeras", "/api/vista/homologia",
                 "/api/vista/homologia/detalle"):
        check(ruta in fuente, "el servidor rutea %s" % ruta)
    # Y la unica que escribe es POST: una vista de lectura detras de un GET no puede cambiar
    # nada ni aunque alguien la llame de mas.
    get, _, post = fuente.partition("def do_POST")
    check("/api/vista/firmar" not in get, "firmar no esta en el camino de GET")
    check("/api/vista/firmar" in post, "firmar es POST")


def main():
    pruebas = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for f in pruebas:
        print("== %s" % f.__name__)
        try:
            f()
        except Exception as e:  # noqa: BLE001
            FALLAS.append("%s levanto %s: %s" % (f.__name__, type(e).__name__, e))
            print("  EXCEPCION %s: %s" % (type(e).__name__, e))

    print()
    print("%d verificaciones" % HECHAS)
    if NO_CORRIDO:
        print()
        print("NO CORRIDO (%d). Un cero aca no significa que este bien: significa que no se "
              "miro." % len(NO_CORRIDO))
        for x in NO_CORRIDO:
            print("   %s" % x)
    if FALLAS:
        print()
        print("FALLARON %d:" % len(FALLAS))
        for x in FALLAS:
            print("   %s" % x)
        return 1
    print("todas las verificaciones pasaron")
    return 0


if __name__ == "__main__":
    sys.exit(main())
