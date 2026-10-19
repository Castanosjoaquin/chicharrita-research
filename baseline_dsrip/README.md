# Baseline dsRIP corrido sobre V-ATPase A

Corrida local del codigo MIT de dsRIP (figshare 10.6084/m9.figshare.28156787, v1.0) sobre el CDS
de V-ATPase A de D. maidis (1.845 nt, reconstruido desde `pipeline/salida/sirna_vatpaseA.csv`).

Entorno: WSL Ubuntu-24.04, Python 3.12, ViennaRNA 2.7.2 (pip), venv en `~/dsrip_dl/venv`.
Codigo de dsRIP bajado a `~/dsrip_dl/code` (solo los 11 archivos .py/.txt/.db necesarios; no se
bajaron las tablas de ortologia).

Dependencias reales que el paper no lista: openpyxl, biopython, pandas, matplotlib, numpy, scipy,
RNAtweaks, orffinder, pysam, brokenaxes, ViennaRNA. RNAtweaks 0.0.2 usa `np.float` (eliminado en
numpy>=1.24): `run_dsrip.py` lo parchea con un shim sin tocar el codigo de dsRIP.
El codigo espera `constant_files/lookup.db` y `constant_files/siRNA_parameters.txt` en el cwd.

Archivos:
- `run_dsrip.py`: corre las funciones reales de dsRIP (solo eficacia; sin off-target).
- `compare.py`, `ablate.py`: comparacion contra `pipeline/salida/sirna_vatpaseA.csv`.
- `dsrip_vatpaseA.csv`: features y total_score de dsRIP por ventana (1.825 filas).
- `dsrip_vatpaseA_regiones.json`: region de 300 pb elegida por `find_best_siRNA_region`.
- `vatpaseA_cds.fasta`: CDS usado como entrada.

Las rutas de los scripts son absolutas de la maquina de Luca; ajustar para reproducir.
