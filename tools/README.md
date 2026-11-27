# Herramientas

Se corren desde la raíz del repo con `python3 tools/NOMBRE.py`. Hace falta la ISO japonesa (SHA-1 `3448ba2ebf69250eb01854f7d1e75d2e18ff987d`) con sus archivos extraídos en `../local/shadow-tower-abyss/iso-jp/`; lo que se genera va en `../local/shadow-tower-abyss/build/` (nunca en el repo). El detalle técnico, en [TECH.md](../TECH.md).

| Herramienta | Qué hace |
|---|---|
| `sta_text.py` | El adaptador del kit. `export` pasa las tablas de texto de `STAZ.STZ` al formato común (`source.jsonl`, campo `ja`) y el inglés fan del PPF a `ref_en.jsonl` (la versión de apoyo, campo `en`); `import` arma `STAZ.STZ` con la traducción de `translation/`; `roundtrip` comprueba que escribir el original deja el archivo idéntico. |
| `exe_text.py` | Los rótulos del ejecutable (`exe#...`): ubica cada campo y su tamaño, exporta con `max` (lo llama `sta_text.py export`) y escribe el ejecutable traducido. `list` muestra los campos; `roundtrip` comprueba que el original queda idéntico. |
| `hooks.py` | Los chequeos propios del juego para `loc.py check`: bytes en Shift-JIS con las letras españolas (T-4), letras que tiene la fuente (T-5) y ancho y renglones de cada caja (T-3). |
| `sta_font.py` | Dibuja las letras españolas en la fuente del juego, con códigos de kanji prestados, y mide el ancho de un renglón. Lo usa `sta_text.py import`. |
| `stz.py` | Lee y rearma el contenedor `STAZ.STZ` con entradas de otro tamaño. |
| `ps2iso.py` | `ps2iso.py ISO_ORIGINAL STAZ_NUEVO ISO_SALIDA [EJECUTABLE]`: mete el contenedor nuevo (y el ejecutable traducido) en una copia de la ISO (ISO9660 y UDF). |
| `pseudo.py` | `pseudo.py ISO_ORIGINAL ISO_SALIDA`: ISO de prueba con todo el texto pseudolocalizado, para ver cortes y glifos que faltan en el juego. |
| `release.py` | `release.py VERSIÓN ISO_ORIGINAL`: arma el paquete de una versión en `../local/shadow-tower-abyss/dist/`. Incluye el parche `.xdelta`, el instalador para Windows (`release/patcher.cs`, compilado con el `csc.exe` de .NET Framework) y `LEEME.txt` (`release/LEEME.txt`). Comprueba el parche y el instalador contra la ISO traducida. Necesita `xdelta3`. |

La entrega es un parche xdelta sobre la ISO japonesa, con un instalador para Windows (`release.py`).
