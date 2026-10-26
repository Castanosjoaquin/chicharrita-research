# Transcripciones crudas del checkpoint 2

Salida sin editar del modelo, para que [`../checkpoint2.md`](../checkpoint2.md) se pueda
auditar cita por cita. **No se corrigió nada acá**: los errores de término técnico, la
diafonía y los tramos incoherentes están tal como salieron. Las correcciones y su
justificación viven en el documento, en la sección «Calidad de la transcripción».

## Cómo se produjeron

Local, sin subir nada a ningún servicio: el audio del investigador y las notas de voz del
equipo se decodificaron y transcribieron en esta máquina.

- **Modelo:** `faster-whisper` 1.2.1 con `large-v3`, `compute_type="int8"`, 8 hilos de CPU.
- **Idioma:** español forzado, VAD activado, `initial_prompt` con el vocabulario del proyecto
  (*Dalbulus maidis*, si-Fi21, off-target, transcriptoma, quimera, y demás) para que el modelo
  no invente variantes de los términos que más se repiten.
- **Decodificación:** `greedy` con `condition_on_previous_text=False` para todos los archivos,
  y una segunda pasada con haz de 5 sobre el audio del investigador.
- **Scripts:** [`transcribe.py`](transcribe.py) y [`decode.py`](decode.py), tal como se
  corrieron. `decode.py` existe porque la versión de PyAV instalada no es compatible con el
  decodificador interno de `faster-whisper`; decodifica a 16 kHz mono y pasa el arreglo
  directo al modelo.

## Los archivos

| Archivo | Origen | Qué es |
| --- | --- | --- |
| [`3-investigador_greedy.txt`](3-investigador_greedy.txt) | `3-audio investigador.m4a`, 7 min 20 s | **La voz del investigador.** Es la fuente que manda |
| [`3-investigador_haz5.txt`](3-investigador_haz5.txt) | el mismo audio | segunda pasada, haz de 5; contra ésta se verificaron las citas |
| [`1-equipo.txt`](1-equipo.txt) | `1-lo que se corto.opus`, 20 s | nota de voz de un compañero |
| [`2-equipo.txt`](2-equipo.txt) | `2-primera_parte que no se grabo.opus`, 1 min 27 s | nota de voz de un compañero |
| [`4-equipo.txt`](4-equipo.txt) | `4-lo que sugiere.opus`, 1 min 1 s | nota de voz de un compañero |
| [`5-equipo.txt`](5-equipo.txt) | `5-final.opus`, 28 s | nota de voz de un compañero |

**Los audios originales no están versionados.** Viven en el `~/Downloads` de quien los grabó.

## Las dos advertencias para quien lea esto

**Los cuatro archivos del equipo no son el investigador.** Se nos pasaron como «lo que
entendió un amigo de la primera parte que no se grabó», pero al transcribirlos resultan ser la
propuesta propia de un compañero, grabada después de la reunión —el audio 4 lo dice: *«un
audio que me acabo de mandar a mí mismo para cerrar una idea»*—. **La primera parte de la
reunión no tiene registro.** En el documento van marcados `[H]` y en una sección aparte.

**Una pasada con haz quedó descartada.** El primer intento con haz de 5 se hizo con el
condicionamiento al texto previo activado y colapsó en un bucle de «Sí» a partir de 02:19.
Se repitió con `condition_on_previous_text=False`, que es la que está acá. Vale como
recordatorio: en audio con diafonía ese condicionamiento hace que el modelo se enganche
repitiendo la última muletilla en vez de transcribir.
