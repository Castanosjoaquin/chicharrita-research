@echo off
REM si-Fi+ — doble clic para abrirlo.
REM
REM El si-Fi21 original, cuando no encuentra su RNAplfold, deja el boton Start sin hacer nada
REM y no dice por que (el UnboundLocalError se lo traga el slot de Qt). Este archivo hace lo
REM contrario: si algo falta, lo escribe y deja la ventana abierta para que se pueda leer.

setlocal
cd /d "%~dp0"

set PY=
for %%P in (py python python3) do (
  if not defined PY (
    %%P --version >nul 2>&1 && set PY=%%P
  )
)

if not defined PY (
  echo.
  echo   No encontre Python en el PATH.
  echo.
  echo   si-Fi+ necesita Python 3.10 o mas nuevo. Instalalo desde python.org
  echo   marcando "Add python.exe to PATH", y volve a hacer doble clic aca.
  echo.
  pause
  exit /b 1
)

%PY% -c "import Bio" 2>nul
if errorlevel 1 (
  echo.
  echo   Faltan las dependencias del port. Corriendo la instalacion:
  echo.
  %PY% -m pip install -r "..\tools\sifi21_port\requirements.txt"
  if errorlevel 1 (
    echo.
    echo   La instalacion fallo. Instalalas a mano con:
    echo     %PY% -m pip install -r tools\sifi21_port\requirements.txt
    echo.
    pause
    exit /b 1
  )
)

%PY% servidor.py %*
if errorlevel 1 pause
endlocal
