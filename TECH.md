# Reglas técnicas

Lo que el juego necesita para que el texto no se rompa. Cada regla tiene un número para citarla, y la mayoría la controla `loc.py check` (el chequeo va entre paréntesis). Salen de cómo está hecho el juego, del adaptador y de la sección 8 del encargo: una traducción nunca puede romper el archivo.

Plantilla del kit: los números quedan; lo de cada regla se completa con lo que muestre la prueba técnica de este juego (PLAN, fase 1). Lo que no aplique se borra.

## Cómo está hecho el juego

Lo que mostró la fase 1 (2026-11-20). Lo que dice *por confirmar* todavía no se probó en el juego.

- **Imagen:** ISO japonesa de 1 561 624 576 bytes, sectores de 2048. Ejecutable `SLPS_252.17`. Casi todo el juego está en `TARGET/STAZ.STZ` (LBA 525217, 253 MB). Los vídeos (`OPENING.PSS`, `PROLOGUE.PSS`, `ENDING.PSS`) y el audio (`*.ADX`) van aparte. `DUMMY.OUT` y `DUMMY01.OUT` (512 MB cada uno) son relleno.
- **`STAZ.STZ`:** cabecera `STAZ` y tabla de 2290 entradas de 32 bytes (`STZ0`, tamaño, tamaño, tamaño con cabecera, 8 bytes de suma, sector de inicio). Cada archivo empieza en su propio sector. El PPF en inglés cambia el contenido sin tocar las sumas, así que el juego probablemente no las comprueba (*por confirmar*).
- **Texto:** tablas `STA ` en Shift-JIS (cp932). Cabecera de 16 bytes y registros `{id, desplazamiento}` (8 bytes) o `{id, nombre, descripción}` (12 bytes), con desplazamientos desde el inicio de la tabla. Cadenas terminadas en `\0`, guardadas seguidas y en el orden de los registros.
  - Tablas sueltas: entradas 15 (`sys/criaturas`), 16 (`sys/objetos`), 17 (`sys/lugares`) y 18 (`sys/menu`).
  - Tablas de los mapas: dentro del bloque `MSGa` de cada `STAM` (entradas 2248 a 2289, `mapa/NNNN`). El bloque guarda en +0x14 el largo de sus datos, que es el espacio disponible. 6 mapas tienen la tabla vacía.
  - Después de la última cadena de muchas tablas de mapa quedan cadenas que ninguna tabla apunta: restos de versiones viejas del texto. No se exportan; el adaptador las conserva y las pisa solo si necesita el espacio.
- **Otro texto** (todavía sin adaptador): unas 900 cadenas japonesas en el ejecutable, texturas con texto (por ejemplo, la entrada 29, `KOKUTI`) y subtítulos dibujados en los vídeos `OPENING.PSS` y `PROLOGUE.PSS`, que el PPF en inglés reemplaza enteros.
- **Reconstrucción:** `tools/stz.py` rearma `STAZ.STZ` con entradas de otro tamaño (cada una en su sector; se conserva la diferencia entre el tamaño y el tamaño con cabecera). `tools/ps2iso.py` lo mete en una copia de la ISO: si crece k sectores, empieza k sectores antes y `DUMMY01.OUT` (relleno, justo antes) pierde esos k sectores. Actualiza ISO9660 y UDF (File Entry con su CRC). El juego abre el archivo por nombre (`\\TARGET\\STAZ.STZ` en el ejecutable), no por sector. Sin cambios, las dos dan archivos idénticos; con todas las tablas sueltas alargadas (+162 KB), el `STAZ.STZ` que sale de la ISO es el nuevo y `PROLOGUE.PSS` queda intacto (2026-11-20). En PCSX2, la ISO de prueba (con el contenedor movido y más grande) arranca, carga la partida y el primer mapa; el juego no comprueba las sumas.
- **Fuente:** entrada 6 (`TTIX`), tres texturas de 512×512 a 4 bits (`dq_FONT`, `dp_FONT`, `ds_FONT`; píxeles desde +0x80 de cada bloque) con ASCII, símbolos, kana y solo los kanji que usa el juego. La tabla de glifos es la entrada 5: el texto Shift-JIS se pasa a Unicode con la tabla estándar del ejecutable y se busca (búsqueda binaria en 0x188910) entre 1002 rangos `{desde, hasta, glifo base}` en Unicode. Cada uno de los 1447 glifos tiene un registro de 24 bytes: u0 v0 u1 v1 en `float` (píxel/511) y cuatro valores: desplazamiento (con signo), ancho, avance y página. Celdas de 22 px de alto; la fuente es proporcional. La página 2 está libre desde y = 332. El juego carga los archivos del contenedor por un identificador de 32 bits (el segundo campo de la «suma» de la tabla), no por número de entrada.
- **Adaptador:** `tools/sta_text.py` (`export`, `import`, `roundtrip`). La ida y vuelta da `STAZ.STZ` idéntico byte por byte (2026-11-20; otra vez el 2026-11-22). El original va en `source.jsonl` con el campo `ja`. El inglés del PPF se aplica en memoria y se exporta aparte a `ref_en.jsonl` (`{key, en}`): 1676 de 1768 textos. Es la versión de apoyo (`support` de `loc.json`): llega a cada línea del lote, solo de consulta (E-1).

## Códigos y saltos

- **T-1** Los códigos (variables, etiquetas, colores, nombres insertados) quedan intactos y en el mismo orden que en el original. Los reconoce la lista `codes` de `loc.json`. (`codigos`)
  - En las tablas `STA ` no hay códigos: el único byte de control es `0x0a` (salto de línea). Falta revisar el texto del ejecutable.
  - Por eso `codes` de `loc.json` queda vacío.
  - El juego no parte los renglones solo: un renglón largo se sale de la caja o de la pantalla (visto en PCSX2, 2026-11-20). Los saltos los pone la traducción.
- **T-2** Saltos de línea: los fijos (`fixed_break` en `loc.json`) van exactamente donde están en el original, ni más ni menos. Los demás, si el adaptador parte los renglones, los pone el adaptador. (`saltos`)
  - Los saltos del japonés están pensados para su ancho, y el juego no parte los renglones solo. No hay saltos fijos (`fixed_break` en `null`): la traducción pone los suyos según el ancho de la caja (T-3).

## Espacio

- **T-3** La caja: ningún renglón puede pasar del ancho que permite el juego. Si el límite medido es el del original y no el de la pantalla, el aviso no obliga a recortar: se permiten abreviaturas reconocibles, pero nunca se quitan palabras ni se acorta de forma que se pierda el sentido. Si la forma completa no cabe, va completa y con su aviso, y se revisa en el juego. [IVA] (chequeo del proyecto, en `hooks`)
  - Medida: el ancho de un renglón es la suma de los avances de sus glifos (`sta_font.width`; las letras españolas avanzan como su letra base). El juego dibuja en un cuadro de 512 de ancho que se estira a 640 en pantalla; el texto va a tamaño 1 (una unidad = un píxel del cuadro) y la línea de botones de abajo, al 70%. Medido con las capturas de los guardados rápidos de PCSX2 (2026-11-20).
  - Cajas (`hooks.box`), en unidades:

    | Texto | Cómo se dibuja | Ancho | Renglones |
    |---|---|---|---|
    | Nombres (objetos, criaturas, lugares) | centrado en la barra de la lista; lo que sobra queda bajo la barra de desplazamiento | 215 | 1 |
    | Descripciones | alineadas a la derecha (x = 499), crecen hacia la izquierda; en los lugares tapan el recuadro «収集率» | 320 | 4 objetos, 3 criaturas y lugares |
    | Ranuras del equipo (`sys/menu` 0079 a 0090) | al 80%, centradas en el panel de la derecha (x ≈ 448); lo que pasa del panel se sale de la pantalla. El original más ancho, `SHORT CUT`, mide 122 | 125 | 1 |
    | Líneas de botones (`○：OK　×：QUIT`…) | al 70%, alineadas a la derecha; los símbolos ○ × △ □ ← → y `：` se ven bien. En la pantalla de título comparten renglón con el copyright (a la izquierda, también al 70%) | 680 | 1 |
    | Resto del menú (ayudas de arriba, ventanas) | alineadas a la derecha o centradas | 480 | — |
    | Mapas | *provisional* [DECISIONS 2026-11-20]: no se llegó a ver un texto de mapa; se confirma en la prueba en el juego (PENDING.md) | 300 | 3 |

  - Con estas cajas el japonés entra entero, salvo `sys/menu#0099` (mensaje de error para los programadores). El inglés fan se pasa en 2 descripciones y en 43 textos de mapa que usan 4 renglones.
- **T-4** Los textos con largo máximo en bytes (`max` en el lote) no pueden pasarlo: es un límite duro. (`bytes`)
  - En Shift-JIS, las letras ASCII ocupan 1 byte y las japonesas 2. No hay límite por texto; el límite es el de cada tabla.
  - Tablas sueltas: no les sobra ningún byte, y antes del archivo siguiente quedan menos de 2 KB de relleno. El inglés del PPF ocupa casi los mismos bytes que el japonés. El español, que suele ser más largo, crece reconstruyendo el contenedor (`tools/stz.py` y `tools/ps2iso.py`), así que en las tablas sueltas no hay límite práctico de bytes.
  - Tablas de los mapas: el `MSGa` va siempre en un bloque `STEM` dentro del mapa (`STAM`, cabecera de 0x40 y bloques seguidos). Si el texto no entra, el `MSGa` crece en múltiplos de 16 y se actualizan los tamaños de `MSGa` (también +8 = tamaño<<8 | 0x43, +0x10 y el largo de datos en +0x14), `STEM` y `STAM`; los bloques siguientes (texturas) solo se corren. Con la pseudolocalización crecen 33 mapas (≈ 57 KB en total). En PCSX2, el primer mapa (`mapa/2248`, +224 bytes) carga y se ve bien, con su tabla crecida en la memoria (guardado rápido, 2026-11-20); falta ver uno de sus textos en pantalla. La estimación con el inglés +20% dice que en 25 de los 34 mapas el español no entraría sin crecer.

## Caracteres

- **T-5** Solo se usan caracteres que tiene la fuente del juego. (`caracteres`, con `hooks.missing_chars`)
  - Letras españolas (`tools/sta_font.py`): á é í ó ú ü ñ Á É Í Ó Ú Ü Ñ ¿ ¡ se dibujan en la página 2 (desde y = 336) a partir de su letra base, con sus medidas (las mayúsculas se achican en vertical para que entre la tilde; ¿ ¡ son ? ! girados). Cada una usa el código de un kanji prestado (`BORROWED`) que tiene glifo, aparece solo en el texto que se traduce y no aparece en el ejecutable; el registro de ese glifo apunta a la letra nueva. No se toca el ejecutable. Cada letra con tilde ocupa 2 bytes. Se ven bien en PCSX2 (2026-11-20).
  - Un kanji prestado escrito tal cual en la traducción no se puede mostrar (se vería la letra española): el chequeo lo marca.
  - Comillas: la fuente tiene `"` y `'` (ASCII). No tiene « » ni la raya —; agregarlas sería otro glifo nuevo.

## Qué se traduce

- **T-6** Lo que no se traduce ni cuenta (restos sin localizar, textos de prueba) va en `excluded` de `loc.json`.
  - Los 46 textos vacíos de `sys/menu`: el juego los dibuja (en la pantalla de título, la de carga y durante el juego), así que un texto puesto ahí aparece en pantalla. Quedan vacíos.
  - Tampoco se tocan el copyright (`sys/menu#0128`), un resto de la demo (`sys/menu#0401`) ni un mensaje de error para los programadores (`sys/menu#0099`). [DECISIONS 2026-11-20]
  - Unos 40 textos ya están en inglés en el original japonés (equipo, `OK`, `CANCEL` y las líneas de botones como `○：OK　×：QUIT`, con `：` y espacio de ancho completo). Se traducen.
- **T-7** Solo se traducen los textos que ve el jugador. Los nombres internos (archivos, etiquetas) no se exportan y no se tocan.
- **T-8** Toda línea del lote se traduce completa: ninguna queda vacía, igual al original ni con frases del original (o del inglés de apoyo) mezcladas. (`vacia`, `sin_traducir`, `ingles_mezclado`, `japones_mezclado`)
