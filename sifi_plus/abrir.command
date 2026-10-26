#!/bin/bash
# si-Fi+ — doble clic para abrirlo en macOS. Es el equivalente de abrir.bat.
#
# Mismo criterio que el .bat: si algo falta, lo escribe y deja la ventana abierta para que
# se pueda leer, en vez de dejar el botón sin hacer nada y no decir por qué.
#
# Tres cosas que en Mac se rompen distinto que en Windows y por eso están acá:
#   1. Finder arranca la Terminal con un PATH mínimo, así que un Python de Homebrew puede
#      existir y no verse. Se agregan sus dos prefijos a mano.
#   2. Un Python instalado por Homebrew rechaza `pip install` con "externally-managed-
#      environment". Cuando pasa, esto arma un entorno propio en .venv-sifi y usa ese.
#   3. El motor RNAplfold 2.1.5 es un .exe que sólo instala si-Fi21 en Windows. Acá no va a
#      estar, y la interfaz lo va a declarar como no disponible: se corre con ViennaRNA.

cd "$(dirname "$0")" || exit 1
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

VENV="$PWD/.venv-sifi"
REQ="../tools/sifi21_port/requirements.txt"

falla() {
  echo
  echo "$@"
  echo
  read -r -p "  Enter para cerrar esta ventana... " _
  exit 1
}

# --- 1. El intérprete -------------------------------------------------------------------
# Si ya hay un entorno propio de una corrida anterior, ese manda: ahí están las
# dependencias. Si no, el primer python3 del sistema que sea 3.10 o más nuevo.

PY=""
if [ -x "$VENV/bin/python3" ]; then
  PY="$VENV/bin/python3"
else
  for cand in python3.13 python3.12 python3.11 python3.10 python3 python; do
    ruta=$(command -v "$cand" 2>/dev/null) || continue
    "$ruta" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' 2>/dev/null || continue
    PY="$ruta"
    break
  done
fi

if [ -z "$PY" ]; then
  falla "  No encontré un Python 3.10 o más nuevo.

  Instalalo desde python.org (el instalador .pkg para macOS) o con Homebrew:
      brew install python@3.12

  Después volvé a hacer doble clic acá."
fi

# --- 2. Las dependencias ----------------------------------------------------------------

faltan=$("$PY" - <<'FIN'
import importlib.util
paquetes = {"Bio": "biopython", "RNA": "ViennaRNA", "numpy": "numpy", "ahocorasick": "pyahocorasick"}
print(" ".join(p for mod, p in paquetes.items() if importlib.util.find_spec(mod) is None))
FIN
)

if [ -n "$faltan" ]; then
  echo
  echo "  Faltan dependencias del port: $faltan"
  echo "  Instalándolas con pip en $PY"
  echo
  if ! "$PY" -m pip install -r "$REQ"; then
    if [ "$PY" = "$VENV/bin/python3" ]; then
      falla "  La instalación falló dentro de $VENV.
  Borrá esa carpeta y volvé a intentar, o instalalas a mano con:
      $PY -m pip install -r tools/sifi21_port/requirements.txt"
    fi
    echo
    echo "  Ese Python no deja instalar (en Mac suele ser el \"externally-managed-environment\""
    echo "  de Homebrew). Armo un entorno propio para si-Fi+ en:"
    echo "      $VENV"
    echo
    "$PY" -m venv "$VENV" || falla "  No pude crear el entorno en $VENV."
    "$VENV/bin/python3" -m pip install --upgrade pip >/dev/null 2>&1
    "$VENV/bin/python3" -m pip install -r "$REQ" || falla \
      "  La instalación falló. Instalalas a mano con:
      $VENV/bin/python3 -m pip install -r tools/sifi21_port/requirements.txt"
    PY="$VENV/bin/python3"
  fi
fi

# --- 3. A correr ------------------------------------------------------------------------

if [ -z "$SIFI_RNAPLFOLD" ]; then
  echo "  Nota: sin SIFI_RNAPLFOLD, el motor RNAplfold 2.1.5 (el de si-Fi21) va a figurar"
  echo "  como no disponible. Se corre con ViennaRNA, y los conteos de los dos motores no"
  echo "  son intercambiables."
  echo
fi

"$PY" servidor.py "$@"
estado=$?
if [ $estado -ne 0 ]; then
  falla "  servidor.py terminó con error (código $estado). El detalle está acá arriba."
fi
