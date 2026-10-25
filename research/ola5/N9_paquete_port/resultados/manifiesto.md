# Manifiesto del paquete del port

Generado por `scripts/armar_manifiesto.py`. 36 archivos.

- `sifi_plus/LEEME.md`
- `sifi_plus/MEJORAS_PROPUESTAS.md`
- `sifi_plus/abrir.bat`
- `sifi_plus/api.py`
- `sifi_plus/complejidad.py`
- `sifi_plus/datos_ejemplo/NM_001111367.2.fasta`  **con nucleotidos (16 hallazgos, todos exceptuados)**
- `sifi_plus/estatico/app.js`
- `sifi_plus/estatico/estilo.css`
- `sifi_plus/estatico/index.html`
- `sifi_plus/exportar.py`
- `sifi_plus/offtarget.py`
- `sifi_plus/perfil.py`
- `sifi_plus/proyecto.py`
- `sifi_plus/servidor.py`
- `sifi_plus/test_api.py`  **con nucleotidos (4 hallazgos, todos exceptuados)**
- `tools/sifi21_port/CAMBIOS.md`
- `tools/sifi21_port/README.md`
- `tools/sifi21_port/alertas.py`
- `tools/sifi21_port/azar_kmer.py`
- `tools/sifi21_port/barrido.py`
- `tools/sifi21_port/conservacion.py`  **con nucleotidos (3 hallazgos, todos exceptuados)**
- `tools/sifi21_port/cruce.py`
- `tools/sifi21_port/ejes_separados.py`
- `tools/sifi21_port/informe_html.py`
- `tools/sifi21_port/offtarget_21nt.py`
- `tools/sifi21_port/panel_y_k.py`
- `tools/sifi21_port/ranking.py`
- `tools/sifi21_port/ranking_v2.py`
- `tools/sifi21_port/requirements.txt`
- `tools/sifi21_port/run_sifi.py`
- `tools/sifi21_port/sifi_core.py`
- `tools/sifi21_port/sifi_energy.py`
- `tools/sifi21_port/test_alertas.py`
- `tools/sifi21_port/test_ejes_separados.py`
- `tools/sifi21_port/test_ranking.py`
- `tools/sifi21_port/test_sifi.py`  **con nucleotidos (10 hallazgos, todos exceptuados)**

## Lo que no va

- `work/` — insumos y salidas con las secuencias del laboratorio; no esta en git
- `research/` — resultados derivados, incluidos los que tocan regiones de EPILAB
- `baseline_dsrip/` — el CDS reconstruido de V-ATPase A (D60)
- `YHat-Biotech/` — el corpus del Investigathon, que es material de ellos
- `pipeline/salida/` — salidas intermedias del pipeline, en .gitignore
