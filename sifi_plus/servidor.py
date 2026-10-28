"""El servidor local. Biblioteca estandar, atado a 127.0.0.1.

Uso:
    python servidor.py                 # abre el navegador solo
    python servidor.py --puerto 8765   # un puerto fijo
    python servidor.py --no-abrir      # no abre nada, para correrlo desde un test

Dos decisiones que no son de comodidad:

**Solo biblioteca estandar.** Nada de Streamlit, Dash ni FastAPI. `requirements.txt` se queda
en sus cuatro lineas, asi que quien pueda correr el port puede correr esto, sin instalar nada
nuevo ni resolver una version.

**Atado a 127.0.0.1, no a 0.0.0.0.** La regla de confidencialidad de `CLAUDE.md` dice que las
secuencias no publicadas no salen de la maquina. Aca eso no es una promesa en un documento: el
socket no escucha en ninguna interfaz de red, asi que no hay a donde salir. Si alguna vez
alguien cambia esta linea, cambia la garantia.

Lo que el servidor NO hace: decidir si una ventana es eficiente. Eso es `sifi_core` y nada
mas. Este archivo rutea, valida la forma de lo que llega y serializa.
"""

from __future__ import annotations

import argparse
import json
import socket
import sys
import threading
import traceback
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import api
import complejidad
import exportar
import offtarget
import proyecto
# Las vistas de lectura de V1. No pasan por `api` ni por el motor: leen archivos versionados
# que escribieron corridas verificadas y los sirven con su etiqueta de procedencia. La unica
# que escribe es `vista_firmas`, y escribe en el archivo de firmas y en ningun otro lado.
import vista_ejes
import vista_firmas
import vista_homologia
import vista_juntura
import vista_marcos
import vista_quimeras
import vista_region

ESTATICO = AQUI / "estatico"
EJEMPLOS = AQUI / "datos_ejemplo"

TIPOS = {".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8",
         ".css": "text/css; charset=utf-8", ".json": "application/json; charset=utf-8",
         ".svg": "image/svg+xml", ".fasta": "text/plain; charset=utf-8",
         ".ico": "image/x-icon"}

# La ultima corrida por gen, para que exportar no obligue al navegador a devolver todo. Es un
# servidor de un solo usuario en localhost: no hay sesiones que aislar.
ULTIMAS: dict[str, dict] = {}
_LOCK = threading.Lock()

COLUMNAS_TABLA = ["pos", "dg_sense5", "dg_antisense5", "ddg", "accessibility",
                  "nt19_at", "nt2_gc", "rama_terminal", "strand_selection",
                  "end_stability", "target_site_accessibility", "thermo_efficient",
                  "is_efficient"]


def columnas(con_seq=False) -> list[str]:
    base = (["pos", "seq"] + COLUMNAS_TABLA[1:]) if con_seq else list(COLUMNAS_TABLA)
    # La complejidad no sale de `sifi_core`: es nuestra, y se agrega al final para no
    # desordenar las columnas que ya estan publicadas en los TSV.
    return base + ["homopolimero", "baja_complejidad"]


def tabla(ventanas, con_seq=False) -> list[list]:
    """La tabla por ventana como lista de listas, que es la mitad del JSON que dicts.

    `seq` sale solo si se pide, igual que el `--con-seq` del CLI: la columna de 21-meros
    sobre ventanas que se solapan de a 1 nt reconstruye el gen entero (C10, ADR D54).
    """
    cols = (["pos", "seq"] + COLUMNAS_TABLA[1:]) if con_seq else COLUMNAS_TABLA
    out = []
    for w in ventanas:
        fila = [getattr(w, c) for c in cols]
        fila.append(complejidad.homopolimero(w.seq))
        fila.append(complejidad.es_baja(w.seq))
        out.append(fila)
    return out


class Handler(BaseHTTPRequestHandler):
    server_version = "sifi_plus"

    # El log por defecto escribe una linea por pedido a stderr, incluido cada archivo
    # estatico. Se silencia lo rutinario y se deja lo que importa.
    def log_message(self, formato, *args):
        pass

    def log_error(self, formato, *args):
        sys.stderr.write("  %s\n" % (formato % args))

    # --- plomeria ---

    def _responder(self, codigo: int, cuerpo: bytes, tipo: str) -> None:
        self.send_response(codigo)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(cuerpo)))
        # Sin cache: durante el desarrollo la pagina cambia todo el tiempo.
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        try:
            self.wfile.write(cuerpo)
        except (BrokenPipeError, ConnectionAbortedError):
            pass  # el navegador cerro la pestana en medio de la respuesta

    def _json(self, datos, codigo=200) -> None:
        self._responder(codigo, json.dumps(datos, ensure_ascii=False,
                                           allow_nan=False, default=str).encode("utf-8"),
                        TIPOS[".json"])

    def _error(self, codigo: int, mensaje: str) -> None:
        self._json({"error": mensaje}, codigo)

    def _cuerpo(self) -> dict:
        n = int(self.headers.get("Content-Length") or 0)
        if not n:
            return {}
        return json.loads(self.rfile.read(n).decode("utf-8"))

    def _estatico(self, rel: str) -> None:
        # Se resuelve y se compara contra la carpeta: sin esto, `..%2f..` sirve cualquier
        # archivo de la maquina. Es un servidor local, pero una travesia de rutas no deja de
        # serlo por eso.
        base = ESTATICO.resolve()
        p = (base / rel).resolve()
        if base not in p.parents and p != base:
            return self._error(403, "fuera de la carpeta de estaticos")
        if not p.is_file():
            return self._error(404, "no existe %s" % rel)
        self._responder(200, p.read_bytes(), TIPOS.get(p.suffix, "application/octet-stream"))

    # --- rutas ---

    def do_GET(self):  # noqa: N802
        ruta = self.path.split("?")[0]
        try:
            if ruta in ("/", "/index.html"):
                return self._estatico("index.html")
            if ruta.startswith("/estatico/"):
                return self._estatico(ruta[len("/estatico/"):])
            if ruta == "/api/arranque":
                return self._json(self._arranque())
            if ruta.startswith("/api/offtarget/"):
                est = offtarget.estado(ruta.rsplit("/", 1)[1])
                return self._json(est) if est else self._error(404, "no hay tal trabajo")
            if ruta == "/api/rangos":
                return self._json({"rangos": proyecto.listar()})
            # --- las vistas de lectura (V1). Todas GET: no cambian nada. ---
            if ruta == "/api/vista/regiones":
                return self._json(vista_region.inventario())
            if ruta == "/api/vista/region":
                q = parse_qs(self.path.partition("?")[2])
                a = (q.get("a") or [""])[0]
                b = (q.get("b") or [""])[0]
                if not a or not b:
                    return self._error(400, "hacen falta las dos regiones del par: ?a=…&b=…")
                return self._json(vista_region.ver(a, b))
            if ruta == "/api/vista/marcos":
                return self._json(vista_marcos.ver())
            if ruta == "/api/vista/juntura":
                return self._json(vista_juntura.ver())
            if ruta == "/api/vista/ejes":
                return self._json(vista_ejes.ver())
            if ruta == "/api/vista/firmas":
                return self._json(vista_firmas.ver())
            if ruta == "/api/vista/quimeras":
                q = parse_qs(self.path.partition("?")[2])
                uno = lambda k, d="": (q.get(k) or [d])[0]  # noqa: E731
                return self._json(vista_quimeras.ver(
                    uno("objetivo", "eficiencia_heredada"),
                    desde=int(uno("desde", "0") or 0),
                    cuantas=int(uno("cuantas", "50") or 50),
                    izquierda=uno("izquierda"), derecha=uno("derecha"),
                    solo_con_alerta=uno("alerta") == "1",
                    l1=int(uno("l1")) if uno("l1") else None))
            if ruta == "/api/vista/quimeras/objetivos":
                return self._json(vista_quimeras.inventario())
            if ruta == "/api/vista/homologia":
                q = parse_qs(self.path.partition("?")[2])
                return self._json(vista_homologia.ver((q.get("ref") or ["HV"])[0]))
            if ruta == "/api/vista/homologia/detalle":
                q = parse_qs(self.path.partition("?")[2])
                uno = lambda k, d="": (q.get(k) or [d])[0]  # noqa: E731
                return self._json(vista_homologia.detalle(
                    uno("ref", "HV"), uno("categoria", "f_reciproco_con_nombre"),
                    desde=int(uno("desde", "0") or 0),
                    cuantas=int(uno("cuantas", "50") or 50),
                    contiene=uno("contiene")))
            return self._error(404, "no hay ruta %s" % ruta)
        except ValueError as e:
            # Un parametro de consulta mal escrito —un objetivo que no existe, una referencia
            # que no esta— es un pedido malformado y no un servidor roto: 400 con el mensaje,
            # que ya enumera los valores validos. Antes caia en el 500 de abajo junto con los
            # errores de verdad, y mezclar las dos cosas esconde las que importan.
            return self._error(400, str(e))
        except Exception as e:  # noqa: BLE001
            traceback.print_exc()
            return self._error(500, "%s: %s" % (type(e).__name__, e))

    def do_POST(self):  # noqa: N802
        ruta = self.path.split("?")[0]
        try:
            cuerpo = self._cuerpo()
        except json.JSONDecodeError as e:
            return self._error(400, "el cuerpo no es JSON valido: %s" % e)
        try:
            if ruta == "/api/diseno":
                return self._json(self._diseno(cuerpo))
            if ruta == "/api/config":
                return self._json(api.parsear_config(cuerpo.get("config", "")))
            if ruta == "/api/offtarget":
                return self._json({"id": offtarget.lanzar(**self._args_offtarget(cuerpo))})
            if ruta == "/api/rangos":
                return self._json(proyecto.guardar(cuerpo))
            if ruta == "/api/exportar":
                return self._json(self._exportar(cuerpo))
            # La unica ruta de esta linea que escribe, y escribe en el archivo de firmas.
            # `FirmaRechazada` hereda de `ValueError`, asi que una firma mal escrita sale como
            # 400 con el motivo —cual de las reglas de D48 no cumple— y no como un 500.
            if ruta == "/api/vista/firmar":
                return self._json(vista_firmas.firmar(
                    clave=cuerpo.get("clave") or "",
                    decision=cuerpo.get("decision") or "",
                    justificacion=cuerpo.get("justificacion") or "",
                    firmado_por=cuerpo.get("firmado_por") or ""))
            return self._error(404, "no hay ruta %s" % ruta)
        except ValueError as e:
            # Parametro fuera de rango o cadena mal escrita: el mensaje ya es para leer.
            return self._error(400, str(e))
        except Exception as e:  # noqa: BLE001
            traceback.print_exc()
            return self._error(500, "%s: %s" % (type(e).__name__, e))

    def do_DELETE(self):  # noqa: N802
        if self.path.startswith("/api/rangos/"):
            ident = self.path.rsplit("/", 1)[1]
            return self._json({"borrado": proyecto.borrar(ident)})
        return self._error(404, "no hay ruta %s" % self.path)

    # --- implementacion de cada ruta ---

    def _arranque(self) -> dict:
        ejemplos = []
        if EJEMPLOS.is_dir():
            for p in sorted(EJEMPLOS.glob("*.fasta")):
                ejemplos.append({"nombre": p.stem, "texto": p.read_text(encoding="utf-8")})
        return {
            "motores": api.motores(),
            "presets": api.PRESETS,
            "defaults": dict(api.DEFAULTS),
            "bases": offtarget.bases_disponibles(),
            "ejemplos": ejemplos,
            "salidas": str(api.SALIDAS),
        }

    def _diseno(self, c: dict) -> dict:
        texto = c.get("secuencia") or ""
        pares = api.leer_fasta(texto)
        if not pares:
            raise ValueError("no encontre ninguna secuencia. Pega un FASTA, o la secuencia "
                             "sola sin encabezado.")

        modo = c.get("modo", "corregido")
        backend = c.get("backend", "vienna")
        if modo not in ("fiel", "corregido"):
            raise ValueError("el modo es 'fiel' o 'corregido'; recibi %r" % modo)
        disp = {m["id"]: m for m in api.motores()}
        if backend not in disp:
            raise ValueError("el motor es 'vienna' o 'exe'; recibi %r" % backend)
        if not disp[backend]["disponible"]:
            raise ValueError(disp[backend]["motivo"])

        off = c.get("off_perfecto")
        mm1 = c.get("off_mm1")
        bandas = c.get("bandas") or []
        con_seq = bool(c.get("con_seq"))

        salida = []
        for nombre, seq in pares:
            ventanas, resumen, contrato = api.correr_diseno(
                seq, nombre=nombre, modo=modo, backend=backend,
                temp_c=float(c.get("temp_c", 22.0)),
                tabla_nn=c.get("tabla_nn", "NN3"),
                largo_region=int(c.get("largo_region", 200)),
                params=c.get("params") or {},
                bandas=bandas, off_perfecto=off, off_mm1=mm1)
            with _LOCK:
                ULTIMAS[nombre] = {"ventanas": ventanas, "resumen": resumen}
            salida.append({
                "contrato": contrato,
                "columnas": columnas(con_seq),
                "tabla": tabla(ventanas, con_seq),
                "baja_complejidad": sorted(complejidad.posiciones_bajas(ventanas)),
            })
        return {"genes": salida}

    def _args_offtarget(self, c: dict) -> dict:
        texto = c.get("secuencia") or ""
        pares = api.leer_fasta(texto)
        if not pares:
            raise ValueError("no hay secuencia de consulta")
        nombre, seq = pares[0]
        size = int(c.get("size", 21))
        mm1 = bool(c.get("mm1"))
        bases = list(c.get("bases") or [])

        # Limite medido, no supuesto: el bowtie de 32 bits del instalador aborta con -v 1 en
        # bases de mas de ~114 MB (M1/REPORT.md §10). Nuestro tamizaje no usa bowtie, pero el
        # costo de las 63 variantes por ventana sobre una base de 984 MB es real, y conviene
        # avisarlo antes de que el usuario espere media hora sin saberlo.
        if mm1:
            grandes = [b for b in offtarget.bases_disponibles()
                       if b["id"] in bases and b["mb"] > 300]
            if grandes:
                raise ValueError(
                    "con un desajuste, %s es demasiado grande para una corrida interactiva "
                    "(%s MB). Corre el tamizaje exacto primero, y el de un desajuste contra "
                    "las bases chicas." % (grandes[0]["nombre"], grandes[0]["mb"]))
        return dict(nombre=nombre, secuencia=seq, bases=bases, size=size,
                    min_block=int(c.get("min_block", min(19, size))), mm1=mm1,
                    ontarget=c.get("ontarget"))

    def _exportar(self, c: dict) -> dict:
        nombre = c.get("gen") or ""
        with _LOCK:
            ultimo = ULTIMAS.get(nombre)
        if not ultimo:
            raise ValueError("no hay una corrida de %r en memoria; volve a correr el "
                             "analisis antes de exportar" % nombre)
        ventanas, resumen = ultimo["ventanas"], ultimo["resumen"]
        que = c.get("que")
        rango = c.get("rango")
        rango = (int(rango[0]), int(rango[1])) if rango else None

        if que == "tsv":
            p = exportar.tsv_por_ventana(ventanas, nombre, con_seq=bool(c.get("con_seq")))
        elif que == "features":
            p = exportar.tsv_por_ventana(ventanas, nombre, solo_features=True)
        elif que == "csv":
            p = exportar.csv_resumen([resumen], nombre)
        elif que == "fasta":
            p = exportar.fasta_sirnas(ventanas, nombre,
                                      solo_eficientes=bool(c.get("solo_eficientes", True)),
                                      rango=rango)
        else:
            raise ValueError("que exportar: tsv, features, csv o fasta; recibi %r" % que)
        return {"ruta": str(p), "bytes": p.stat().st_size}


def puerto_libre(preferido: int = 8731) -> int:
    """El preferido si esta libre; si no, uno que el sistema elija."""
    for p in (preferido, 0):
        s = socket.socket()
        try:
            s.bind(("127.0.0.1", p))
            return s.getsockname()[1]
        except OSError:
            continue
        finally:
            s.close()
    raise SystemExit("no pude tomar ningun puerto en 127.0.0.1")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--puerto", type=int, default=None)
    ap.add_argument("--no-abrir", action="store_true", help="no abrir el navegador")
    a = ap.parse_args(argv)

    puerto = a.puerto or puerto_libre()
    url = "http://127.0.0.1:%d/" % puerto

    print("si-Fi+ — el port de si-Fi21 con interfaz")
    print()
    for m in api.motores():
        print("  motor %-7s %s" % (m["id"], m["nombre"] if m["disponible"]
                                   else "NO disponible — " + m["motivo"]))
    bases = offtarget.bases_disponibles()
    print("  bases de off-target: %d en disco" % len(bases))
    print("  las salidas se escriben en %s" % api.SALIDAS)
    print()
    print("  abierto en %s" % url)
    print("  (Ctrl+C para cortar)")
    print()

    servidor = ThreadingHTTPServer(("127.0.0.1", puerto), Handler)
    if not a.no_abrir:
        threading.Timer(0.4, webbrowser.open, args=(url,)).start()
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\ncortado")
    finally:
        servidor.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
