# V2 — Las dos pestañas que V1 dejó afuera

Issue **#46**, continuación de `V1` (issue #45). Antecedentes: `O4` (enumerador de quimeras),
`F1` (transferencia por homología), `D63`, `D78`, `D89`, y el preregistro de la línea en
`sifi_plus/PREREGISTRO_DEMO.md`, ampliado y commiteado antes del primer renglón de código
(`742ed17`).

## 1. Por qué existe esta línea

`V1` excluyó por alcance cuatro cosas, entre ellas el enumerador de quimeras y la transferencia
por homología. Revisado con el usuario, **esas dos eran justamente las que hacían falta**, y el
motivo escrito de la exclusión no se sostiene para ellas.

El motivo decía que las otras «ya están servidas en HTML» y que el enumerador es «una corrida de
~71 días y un botón ahí sería una mentira». Lo segundo es cierto **sobre correr el enumerador**,
y no sobre mostrar lo que ya corrió: medido en disco, las 3.204 quimeras admisibles **ya están
enumeradas y escritas** `[M]`. El alcance de `V1` mezcló «no pongas un botón que lo corra» con «no
muestres el resultado», que son dos cosas distintas. La primera sigue vigente —no hay ningún
botón que corra nada— y la segunda se levanta acá.

Vale la pena dejarlo escrito porque es un modo de equivocarse que se repite: un argumento
correcto sobre el **costo de producir** un resultado se arrastra como si fuera un argumento sobre
el **costo de mostrarlo**, y no lo es.

## 2. Lo que quedó mostrado

Dos pestañas nuevas, las dos de lectura. La interfaz pasa de ocho a diez.

**Vista F — enumerador de quimeras.** Lee los tres pares TSV + JSON de
`research/ola6/O4_enumerador_quimeras/resultados/`, uno por objetivo, de **3.204 filas × 35
columnas** cada uno `[M]`. Muestra la grilla y su poda —de 47.833.512 combinaciones a 3.204
admisibles, paso 50— la tabla en el orden del archivo, y filtros por gen de cada lado, por largo
del fragmento izquierdo y por si el empalme fabrica alerta nueva. De las 3.204, **515 fabrican
alerta de juntura nueva** `[M]`.

**Vista G — transferencia por homología.** Lee `resumen_lectura.json`, `resumen.json`,
`controles.json` y el detalle por ORF de `transferencia_HV.tsv.gz` / `_MQ.tsv.gz` de
`research/ola6/F1_transferencia_homologia/resultados/`. Muestra el embudo de seis categorías, las
dos variantes, los controles y el detalle paginado.

El embudo de `HV`, contado sobre el archivo `[M]`:

| Categoría | ORF |
|---|---|
| `a_sin_orf` — el contig no tiene ORF de largo suficiente | 25.812 |
| `b_sin_hit` — el ORF no tiene hit | 76.476 |
| `c_hit_no_reciproco` — tiene hit, la inversa no vuelve | 10.118 |
| `d_empate` — la inversa vuelve empatada | 13.623 |
| `e_reciproco_sin_nombre` — recíproco, sin nombre informativo | 1.472 |
| **`f_reciproco_con_nombre`** — **se le puede poner nombre** | **4.182** |

Las dos últimas suman 5.654, que son los ORF recíprocos que declara el resumen, y la última es
exactamente su cifra de ORF con nombre: el embudo cierra contra el resumen `[M]`.

## 3. Las dos reglas nuevas, que son los dos modos de romper la regla de la línea

Estas dos vistas traen riesgos que las cinco de `V1` no tenían, y el preregistro los fijó antes
de escribir el código.

**En quimeras, el orden ES el criterio.** Los tres objetivos son **las mismas 3.204 quimeras
ordenadas distinto** —verificado: los tres conjuntos son idénticos y el primer puesto cambia
entre ellos `[M]`—. Así que el primer puesto de un objetivo es la respuesta de ese objetivo, no
una propiedad de la quimera. La vista muestra el orden del archivo, **no reordena por un índice
propio y no combina los objetivos**. Y hay un detalle que importa más de lo que parece: la
columna `#` es **el puesto en el archivo, no la posición en lo filtrado**. Al filtrar por alerta
los números salen `11, 13, 19` y eso es correcto; renumerarlos desde 1 convertiría el filtro en
un criterio.

**La advertencia del archivo viaja arriba de la tabla, no al pie.** El JSON declara que «el
criterio de eficiencia de si-Fi21 no está validado en hemípteros: rho = +0,142, IC95 [-0,247,
+0,492], n = 29». Eso califica **todas** las columnas de eficiencia de la vista. Una tabla de
3.204 quimeras ordenadas por eficiencia invita a leer el primer puesto como una recomendación, y
no lo es.

**En homología, la cifra de cabecera es la variante preregistrada.** Hay dos, y la diferencia no
es menor: `estricta_preregistrada` da 5.654 ORF recíprocos en `HV` y 5.936 en `MQ`;
`ampliada_H_post_hoc` da 11.058 y 12.269 `[M]`. La ampliada se definió **después de ver los
datos** y rinde más del doble. Las dos se muestran con su rótulo, y de cabecera va la
preregistrada. Poner la ampliada porque es más grande sería elegir el número después de verlo,
que es justamente lo que un preregistro existe para impedir.

**Y el control positivo no pasa la variante estricta.** El ORF de la subunidad B de la V-ATPasa
—que se sabe que está, con 100 % de identidad— cae en `d_empate` en la estricta y sólo pasa en la
ampliada (`pasa_estricta: false`, `pasa_ampliada: true`) `[M]`. Es el dato que más califica la
lectura de toda la vista, así que va **junto a la cifra** y no en una nota al pie: el criterio
preregistrado deja afuera un caso que debería atrapar. El señuelo, en cambio, sale limpio —0 de
1.000 consultas con hit en las dos referencias `[M]`— así que el método no está inventando
homología donde no hay.

## 4. La procedencia pidió un campo distinto, y se declaró

Homología es el primer caso donde el contrato de procedencia no encaja tal cual. **No lleva modo
ni motor: `no aplica`.** Una transferencia por homología no pasa por el criterio de eficiencia de
si-Fi ni por RNAplfold — la hace DIAMOND 2.2.8 contra dos proteomas —. El campo que ocupa el lugar
del panel son las **dos referencias con su SHA-256**, leídas de `resumen.json`.

La alternativa era dejar los tres campos vacíos, y habría sido peor: un sello vacío se lee como
«se olvidaron de llenarlo» y no como «esta cifra no tiene modo». Son dos de los cuatro estados
que el preregistro distingue, y mezclarlos es el error que el contrato existe para evitar.

## 5. Las verificaciones

`python test_api.py` pasa de **189** a **246 verificaciones**, todas en verde, con los mismos
cinco bloques «no corrido» antes y después `[M]`. Los conteos ancla no se movieron: las vistas no
llaman al motor.

Las verificaciones nuevas son dos, y miran exactamente las dos reglas de arriba:

- **`test_las_quimeras_no_se_reordenan`** — que los tres objetivos traigan las mismas quimeras,
  que el primer puesto cambie entre ellos, que las primeras cinco filas salgan en el orden del
  archivo, que el puesto sea la posición en el archivo y que el filtro **conserve** ese puesto en
  vez de renumerar. Más que la advertencia viaje con la tabla y que la grilla declare cuánto podó.
- **`test_la_homologia_distingue_lo_preregistrado_de_lo_post_hoc`** — que haya exactamente una
  variante de cabecera, que sea la preregistrada, que la post hoc **rinda más y aun así no sea la
  de cabecera**, que el control positivo declare si pasa la estricta, que la procedencia diga «no
  aplica» en modo y motor, que el embudo cierre contra el resumen, y que el detalle se pagine —un
  tope absurdo se recorta a 500 y no vuelca las 131.683 filas—.

Y las verificaciones que ya estaban se extendieron para cubrir las dos vistas nuevas: no importan
el motor, no tienen ninguna llamada de escritura, no cambian la huella de ninguno de los catorce
archivos que leen, y un insumo ausente produce «no corrido» sin una sola cifra.

### Un defecto que apareció al probar las rutas

`do_GET` no atrapaba `ValueError`, así que un parámetro de consulta mal escrito —un objetivo que
no existe, una referencia que no está— caía en el `500` genérico junto con los errores de verdad.
Ahora devuelve **400** con el mensaje, que ya enumera los valores válidos. No es de estas vistas
—el defecto estaba desde antes y lo heredaban las cinco de `V1`— pero lo destaparon ellas porque
son las primeras con parámetros de consulta validados.

## 6. Lo que no se pudo mostrar

1. **El panel de referencias de `O4`.** El JSON declara modo, motor, tabla, temperatura, grilla,
   plegados y qué busca el tamizado de juntura, pero **no las referencias contra las que tamizó**
   `[M]`. La vista lo muestra como «procedencia no declarada». Es el mismo hueco que `V1`
   encontró en `M6` y en los ejes de `O3`: van tres archivos distintos sin panel declarado, lo que
   sugiere que conviene una convención de sidecar y no un parche por línea.
2. **La grilla fina de paso 10.** Existe —169.648 combinaciones, 4,7 MB comprimidos— y no entra a
   la vista: son dos órdenes de magnitud más filas y si se reparte entre máquinas o se archiva es
   una decisión abierta (`D89`, issue #42). La vista nombra el archivo y dice por qué no lo carga.
3. **La v1 de homología**, que no es un hueco sino una exclusión deliberada: su propio archivo
   declara `estado: "v1 DESCARTADA POR SU PROPIO CONTROL: no se lee"`. La vista la nombra como
   descartada y no la lee.

## 7. Los archivos

| Archivo | Qué es |
|---|---|
| `sifi_plus/PREREGISTRO_DEMO.md` | ampliado con las dos vistas, commiteado antes del código |
| `sifi_plus/vista_quimeras.py` | vista F, el enumerador leído de disco |
| `sifi_plus/vista_homologia.py` | vista G, el embudo, las dos variantes y los controles |
| `sifi_plus/servidor.py` | cuatro rutas nuevas, todas GET, y el `400` de parámetros |
| `sifi_plus/estatico/app.js` | el dibujo de las dos vistas |
| `sifi_plus/test_api.py` | 246 verificaciones, de 189 |
