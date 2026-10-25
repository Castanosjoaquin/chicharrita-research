# N9 — El paquete del port, acotado y verificado

**Ola 5, línea N9.** Fecha: 2026-10-25. Cierra la promesa de nuestra carta —«dejanos hacerle antes
una revisión, porque el repositorio tiene resultados derivados de las secuencias de EPILAB»— con
el alcance que fijó la respuesta del investigador: «me interesa conocer su implementación, pero no
necesitan compartir datos internos de EpiLab ni archivos intermedios de sus diseños» `[R]`.

## El resultado, en un párrafo

`[M]` El paquete son **36 archivos**: los dos directorios completos, `tools/sifi21_port/` y
`sifi_plus/`, con su código, sus pruebas y sus dos LEEME. No hay un solo resultado derivado
adentro: ningún TSV, ningún JSON de corrida, ninguna figura de una corrida sobre las secuencias del
laboratorio. **Cuatro de los 36 contienen nucleótidos y los cuatro están exceptuados con su fuente
pública escrita**, y el paquete da **cero hallazgos sin exceptuar** en las dos pasadas de
`tools/verificacion/sin_secuencias.py` `[M]`.

| Archivo | Qué tiene adentro | Por qué es público |
|---|---:|---|
| `sifi_plus/datos_ejemplo/NM_001111367.2.fasta` | 16 | el ARNm de la ferredoxina-6 de *Zea mays*, RefSeq, con su accesión en el encabezado |
| `tools/sifi21_port/test_sifi.py` | 10 | fixtures: el ejemplo del docstring de `free_energy3` del si-Fi21 original y secuencias de control |
| `tools/sifi21_port/conservacion.py` | 3 | los cebadores de la Tabla 1 de Andrada *et al.* 2026, publicada |
| `sifi_plus/test_api.py` | 4 | fixtures del criterio de baja complejidad: poli-A, un dinucleótido alternado y un 21-mero sintético |

`[M]` Las cuatro pasaron la verificación contra la planilla de EPILAB con cero coincidencias, que
es la pasada que distingue una fuga de un dato público. Y hay una decisión vieja que conviene
recordar acá porque es exactamente la que se aplica: el dato de ejemplo de la interfaz es maíz y no
el genoma del MRFV **a propósito**, porque `NC_002786.2` cubre el 90,5 % de `MP_MRFV` y el 96,5 %
de `CP_MRFV`, y mandarle al investigador una herramienta que trae adentro dos de sus cuatro
regiones invita justamente la conversación que la revisión venía a evitar.

## Lo que no va, y por qué

| Fuera | Motivo |
|---|---|
| `work/` | insumos y salidas con las secuencias del laboratorio; además no está en git |
| `research/` | resultados derivados, incluidos los dos archivos con 28 ventanas de EPILAB que D61 decidió dejar como están |
| `baseline_dsrip/` | el CDS reconstruido de V-ATPase A (D60) |
| `YHat-Biotech/` | el corpus del Investigathon, que es material de ellos |
| `pipeline/salida/` | salidas intermedias, en `.gitignore` |

`[H]` La distinción importa y es la que D61 dejó anotada: dar acceso al repositorio entero **no es**
lo mismo que entregar este paquete. Los fragmentos que D61 decidió conservar en el árbol viven en
`research/`, así que quedan afuera del paquete por construcción. Si alguna vez se compartiera el
repositorio completo en vez del paquete, esa decisión hay que releerla.

## Cómo se reproduce

```
python tools/verificacion/sin_secuencias.py --json <ruta libre>/verif.json
python research/ola5/N9_paquete_port/scripts/armar_manifiesto.py <ruta libre>/verif.json
```

El script **aborta** si alguna ruta del paquete cae en la lista de lo que no va, o si aparece un
hallazgo de nucleótidos sin exceptuar. El manifiesto queda en `resultados/manifiesto.md`.

## Lo que queda por decidir, y no lo decide un script

`[?]` **Cómo se entrega.** Un .zip, un repositorio aparte o acceso de lectura a un clon acotado.
Armar el paquete es una decisión del equipo y el usuario; esta línea deja el manifiesto y la
constancia, no el archivo.

`[?]` **La licencia del si-Fi21 original.** El port reimplementa un criterio publicado y no copia
código, pero la pregunta de licencia pesa al publicar y no al mostrarle el port a su autor, así
que no bloquea la reunión. Queda viva para cualquier publicación posterior.

`[M]` **Una limitación operativa de la máquina, que no es del paquete.** El gancho de pre-commit
llama a `python3`, y en esta máquina ese intérprete no tiene `openpyxl` mientras el de Anaconda sí.
El gancho rechaza entonces con «no se pudo verificar», que es el comportamiento correcto —es
fail-closed—, pero obliga a correr las dos pasadas a mano con el intérprete que tenga la
dependencia. Está anotado en `PREGUNTAS_ABIERTAS.md`.

## Archivos

| Archivo | Qué es |
|---|---|
| `scripts/armar_manifiesto.py` | enumera el paquete, lo cruza con la verificación y aborta si algo no cierra |
| `resultados/manifiesto.md` | los 36 archivos, los cuatro con nucleótidos marcados, y lo que queda afuera |
