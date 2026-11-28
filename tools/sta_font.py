#!/usr/bin/env python3
"""Letras españolas en la fuente de Shadow Tower Abyss.

Cómo dibuja el juego (TECH.md, T-5): el texto en Shift-JIS se pasa a Unicode
con la tabla estándar del ejecutable, y el Unicode se busca en la entrada 5 de
STAZ.STZ (rangos {desde, hasta, glifo base} y registros de glifo de 24 bytes:
u0 v0 u1 v1 en float, con píxel/511, y cuatro u16: desplazamiento, ancho,
avance y página; el desplazamiento lleva signo). Las tres páginas son las texturas de 512×512 a 4 bits de la
entrada 6 (dq_FONT, dp_FONT, ds_FONT); la página 2 está libre desde y = 332.

Shift-JIS no tiene letras españolas. Cada una toma el código de un kanji que
solo aparece en el texto que se traduce (nunca en el ejecutable), y el
registro de ese glifo pasa a apuntar a la letra nueva, dibujada en el espacio
libre de la página 2 con las medidas de su letra base. No se toca el ejecutable
ni cambia el tamaño de ningún archivo.

Cada página tiene su propia paleta de 16 tonos (RGBA, todos del mismo gris y
con distinta opacidad), guardada detrás de sus píxeles y en otro orden que las
demás. Por eso la letra se copia por opacidad, no por índice: cada píxel toma
el tono de la página 2 más parecido al de la página de origen.

    python3 tools/sta_font.py preview SALIDA.png   # muestra los glifos nuevos
"""
import struct

SPANISH = "áéíóúüñÁÉÍÓÚÜÑ¿¡"
# Kanji prestados (en orden de SPANISH). Condición: tienen glifo, aparecen en
# las tablas de texto y no aparecen en el ejecutable (se comprueba en check()).
BORROWED = "亜闇以囲為域一稲隠雨永越怨演焔奥"
CHARMAP = dict(zip(SPANISH, BORROWED))
BASE = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ü": "u", "ñ": "n",
        "Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U", "Ü": "U", "Ñ": "N",
        "¿": "?", "¡": "!"}

FONT_TABLE, FONT_TEX = 5, 6
PAGE_PIX = (0x100 + 0x80, 0x20280 + 0x80, 0x40400 + 0x80)
CLUT = 0x20000 + 0x80   # paleta (16 × RGBA) desde los píxeles de cada página
H = 22            # alto de celda
FREE_Y = 336      # primera fila libre usada en la página 2
U = 511.0


def encode(text):
    """Texto en español -> bytes Shift-JIS que entiende el juego."""
    return "".join(CHARMAP.get(ch, ch) for ch in text).encode("cp932")


def missing(text):
    """Caracteres que el juego no puede mostrar (incluye los kanji prestados,
    que en el juego se ven como la letra española que ocupa su lugar)."""
    out = []
    for ch in text:
        if ch in CHARMAP or ch == "\n":
            continue
        if ch in BORROWED:
            out.append(ch)
            continue
        try:
            ch.encode("cp932")
        except UnicodeEncodeError:
            out.append(ch)
    return out


class Font:
    def __init__(self, table, tex):
        self.t = bytearray(table)
        self.x = bytearray(tex)
        self.nr, self.ng = struct.unpack_from("<HH", self.t, 0x10)
        self.ro, self.go = struct.unpack_from("<II", self.t, 0x14)
        self.ranges = [struct.unpack_from("<3H", self.t, self.ro + 6 * i) for i in range(self.nr)]
        self.alpha = [[self.x[o + CLUT + 4 * i + 3] for i in range(16)] if len(self.x) > o + CLUT + 64
                      else None for o in PAGE_PIX]

    def glyph_index(self, ch):
        u = ord(ch)
        for lo, hi, base in self.ranges:
            if lo <= u <= hi:
                return base + u - lo
        return None

    def rec(self, g):
        return list(struct.unpack_from("<4fh3H", self.t, self.go + 24 * g))

    def set_rec(self, g, r):
        struct.pack_into("<4fh3H", self.t, self.go + 24 * g, *r)

    def px(self, page, x, y):
        v = self.x[PAGE_PIX[page] + (y * 512 + x) // 2]
        return (v >> 4) if x & 1 else (v & 15)

    def put(self, page, x, y, val):
        o = PAGE_PIX[page] + (y * 512 + x) // 2
        v = self.x[o]
        self.x[o] = (v & 0x0F) | (val << 4) if x & 1 else (v & 0xF0) | val

    def opacity(self, page, x, y):
        """Opacidad del píxel (0–255), según la paleta de su página."""
        return self.alpha[page][self.px(page, x, y)]

    def put_opacity(self, page, x, y, a):
        """Escribe el tono de la página con la opacidad más parecida a `a`."""
        pal = self.alpha[page]
        self.put(page, x, y, 0 if a <= 0 else min(range(1, 16), key=lambda i: abs(pal[i] - a)))

    def bitmap(self, ch):
        """Opacidades (0–255) de la celda del glifo, y su registro."""
        r = self.rec(self.glyph_index(ch))
        x0, y0, w = round(r[0] * U), round(r[1] * U), round((r[2] - r[0]) * U)
        return [[self.opacity(r[7], x0 + x, y0 + y) for x in range(w)] for y in range(H)], r


# Opacidades (0–255): desde cuánto cuenta como tinta, y los tonos de los signos
# (el centro del trazo de la fuente es casi opaco; el borde, intermedio).
INK = 70
SOLID = 238
EDGE = 115


def _ink_cols(bm, rows):
    cols = [x for x in range(len(bm[0])) if any(bm[y][x] > INK for y in rows)]
    return (min(cols), max(cols)) if cols else (0, len(bm[0]) - 1)


def _dot(bm, x, y, v):
    if 0 <= y < H and 0 <= x < len(bm[0]):
        bm[y][x] = max(bm[y][x], v)


SS = 4            # supermuestreo de los signos


def _stroke(bm, points, width):
    """Traza una línea suave (con antialias) por `points` (en píxeles de la
    celda, con decimales) y la suma a la celda. Se dibuja a SS veces el tamaño
    y se reduce: los signos trazados píxel a píxel se veían como cuentas, y la
    sombra que el juego pone abajo a la derecha asomaba entre ellas como
    puntitos negros (prueba del 2026-11-28)."""
    from PIL import Image, ImageDraw
    w = len(bm[0])
    im = Image.new("L", (w * SS, H * SS), 0)
    d = ImageDraw.Draw(im)
    pts = [(x * SS + SS / 2, y * SS + SS / 2) for x, y in points]
    r = width * SS / 2
    d.line(pts, fill=255, width=max(1, round(width * SS)), joint="curve")
    for x, y in (pts[0], pts[-1]):
        d.ellipse((x - r, y - r, x + r, y + r), fill=255)
    small = im.resize((w, H), Image.BOX).load()
    for y in range(H):
        for x in range(w):
            v = small[x, y] * SOLID // 255
            if v:
                bm[y][x] = max(bm[y][x], v)


def _acute(bm, cx, top, steps=4):
    # trazo inclinado como la cursiva de la fuente: de abajo a la izquierda a arriba a la derecha
    # grosor 2: como los trazos de las letras (con 1.6 se veía más fina y clara)
    _stroke(bm, [(cx - 0.3, top + steps - 1), (cx + steps - 0.7, top)], 2.0)


def _diaeresis(bm, cx, top):
    for x in (cx - 2, cx + 2):
        _stroke(bm, [(x + 0.5, top + 1.5), (x + 0.5, top + 1.6)], 1.9)


def _tilde(bm, cx, top):
    # virgulilla ondulada de 9 px centrada en cx (una onda entera)
    import math
    pts = [(cx - 4 + 8 * t / 16, top + 1.2 - 0.9 * math.sin(2 * math.pi * t / 16)) for t in range(17)]
    _stroke(bm, pts, 1.9)


def make_glyph(font, ch):
    base = BASE[ch]
    bm, r = font.bitmap(base)
    w = len(bm[0])
    if ch in "¿¡":
        return [row[::-1] for row in bm[::-1]], r
    lower = base.islower()
    if lower:
        for y in range(0, 7):           # quita el punto de la i
            bm[y] = [0] * w
        top_rows = range(8, 11)
        mark_top = 3
    else:
        # mayúscula: se achica en vertical para dejar 4 filas arriba
        ink = [y for y in range(H) if any(v > 40 for v in bm[y])]
        y0, y1 = min(ink), max(ink)
        new_top = 4
        out = [[0] * w for _ in range(H)]
        for y in range(new_top, y1 + 1):
            src = y0 + (y - new_top) * (y1 - y0) / max(1, (y1 - new_top))
            sy = min(y1, round(src))
            out[y] = list(bm[sy])
        bm = out
        top_rows = range(new_top, new_top + 3)
        mark_top = 0
    lo, hi = _ink_cols(bm, top_rows)
    cx = (lo + hi) // 2
    if ch in "áéíóú":
        _acute(bm, cx - 1, mark_top)
    elif ch in "ÁÉÍÓÚ":
        _acute(bm, cx, mark_top, 3)
    elif ch in "üÜ":
        _diaeresis(bm, cx, mark_top)
    elif ch in "ñÑ":
        _tilde(bm, cx, mark_top)
    return bm, r


def apply(table, tex):
    """Devuelve (tabla nueva, textura nueva) con las letras españolas."""
    f = Font(table, tex)
    x = 0
    for ch in SPANISH:
        bm, r = make_glyph(f, ch)
        w = len(bm[0])
        y = FREE_Y + (x + w > 511) * (H + 1)
        if x + w > 511:
            x = 0
        for yy in range(H):
            for xx in range(w):
                f.put_opacity(2, x + xx, y + yy, bm[yy][xx])
        g = f.glyph_index(CHARMAP[ch])
        f.set_rec(g, [x / U, y / U, (x + w) / U, (y + H) / U, r[4], r[5], r[6], 2])
        x += w + 1
    return bytes(f.t), bytes(f.x)


def advances(table):
    """{carácter: avance} de todos los glifos de la fuente. Las letras
    españolas avanzan lo mismo que su letra base (make_glyph)."""
    f = Font(table, b"")
    out = {}
    for lo, hi, base in f.ranges:
        for u in range(lo, hi + 1):
            out[chr(u)] = f.rec(base + u - lo)[6]
    for ch in SPANISH:
        out[ch] = out[BASE[ch]]
    return out


def width(text, adv):
    """Ancho de un renglón en unidades de la fuente (TECH.md, T-3)."""
    return sum(adv.get(ch, 0) for ch in text)


def check(stz_body, exe, source_chars):
    """Comprueba que los kanji prestados sirven (ver BORROWED)."""
    f = Font(stz_body(FONT_TABLE), stz_body(FONT_TEX))
    bad = []
    for ch in BORROWED:
        if f.glyph_index(ch) is None:
            bad.append((ch, "sin glifo"))
        if ch.encode("cp932") in exe:
            bad.append((ch, "aparece en el ejecutable"))
        if ch not in source_chars:
            bad.append((ch, "no aparece en el texto"))
    return bad


if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from stz import Stz
    import sta_text
    c = Stz(open(sta_text.STZ, "rb").read())
    if len(sys.argv) == 3 and sys.argv[1] == "preview":
        from PIL import Image
        table, tex = apply(c.body(FONT_TABLE), c.body(FONT_TEX))
        f = Font(table, tex)
        words = ["áéíóú üñ ÁÉÍÓÚ ÜÑ ¿¡", "¿Dónde está la caña?", "¡Acción! Pingüino, ÉXITO, Ñandú"]
        img = Image.new("L", (760, 40 + 30 * len(words)), 0)
        crop = Image.new("L", (512, 26))
        for yy in range(26):
            for xx in range(512):
                crop.putpixel((xx, yy), f.opacity(2, xx, FREE_Y - 2 + yy))
        img.paste(crop, (4, 4))
        for i, wd in enumerate(words):
            pen = 8
            for ch in "".join(CHARMAP.get(c2, c2) for c2 in wd):
                r = f.rec(f.glyph_index(ch))
                x0, y0, w = round(r[0] * U), round(r[1] * U), round((r[2] - r[0]) * U)
                for yy in range(H):
                    for xx in range(w):
                        v = f.opacity(r[7], x0 + xx, y0 + yy)
                        if v:
                            p = (pen + r[4] + xx, 36 + 30 * i + yy)
                            img.putpixel(p, max(img.getpixel(p), v))
                pen += r[6]
        img = img.resize((img.width * 2, img.height * 2), Image.NEAREST)
        img.save(sys.argv[2])
        print("vista previa ->", sys.argv[2])
    else:
        print(__doc__)
