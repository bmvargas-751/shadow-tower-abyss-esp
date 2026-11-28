#!/usr/bin/env python3
"""Texturas con texto de Shadow Tower Abyss (TECH.md, «Texturas»).

Las texturas van en archivos TTIX dentro de STAZ.STZ: cabecera de 16 bytes
(`TTIX`, tamaño, cantidad) y un registro de 0x50 bytes por textura: nombre
(8 bytes), posición de los píxeles (+8), posición de la paleta (+0x24) y el
registro TEX0 del GS (+0x40: formato, ancho y alto). Píxeles y paleta van detrás
de una cabecera de 0x80 bytes, sin entrelazar. Las de 8 bits llevan 256 colores
RGBA (alfa hasta 0x80) en el orden CSM1 del GS.

Las pantallas (entradas 19 a 25) recortan cada palabra de su textura con un
rectángulo fijo (ancho, alto, u, v en píxeles). La traducción redibuja cada
palabra dentro de su mismo rectángulo, con la fuente del juego (la de los
textos, con las letras españolas de sta_font) [DECISIONS 2026-11-28]: se borra
el rectángulo, se escribe el texto con su sombra, se estrecha a lo ancho si no
entra y cada píxel toma el color más parecido de la paleta de la textura. Nada
cambia de tamaño.

    python3 tools/sta_tex.py preview CARPETA   # PNG de las texturas, antes y después
"""
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sta_font  # noqa: E402

ENTRY = 29     # TTIX con KOKUTI, STFE_010..014, STFE_110..120 y STSH_004

# {textura: [(u, v, ancho, alto, texto)]} (\\n separa renglones). Rectángulos de la
# plantilla de la enciclopedia y el equipo (entrada 22). Las de STFE_014 son
# los nombres de las estadísticas (el original ya los trae en inglés, T-6).
WORDS = {
    "STFE_014": [
        (0, 0, 57, 16, "Aguante"),            # Stamina (身)
        (56, 0, 53, 16, "Vitalidad"),         # Vitality (地)
        (108, 0, 59, 16, "Fuerza"),           # Strength (甲)
        (166, 0, 69, 16, "Destreza"),         # Dexterity
        (0, 16, 38, 16, "Corte"),             # Slash (断; 斬撃 → corte)
        (38, 16, 39, 16, "Aplastar"),         # Break (砕; 破砕 → aplastar)
        (77, 16, 41, 16, "Estocada"),         # Pierce (貫; 刺突 → estocada)
        (118, 16, 45, 16, "Magia"),           # Magic (気)
        (162, 16, 94, 16, "Concentración"),   # Concentration (詠)
        (0, 32, 70, 16, "Mentalidad"),        # Mentality (陣)
        (70, 32, 40, 16, "Mente"),            # Mind (浄)
        (110, 32, 54, 16, "Partícula"),       # Element (粒, clase de magia)
        (164, 32, 50, 16, "Disolución"),      # Solvent (溶, clase de magia)
        (214, 32, 38, 16, "Espíritu"),        # Spirit (霊, clase de magia)
        (0, 48, 68, 16, "Durabilidad"),       # Durability (耐)
        (68, 48, 48, 16, "Peso"),             # Weight (重量)
        (116, 48, 82, 16, "Peso total"),      # Total weight (総重量)
    ],
    "STFE_012": [
        (58, 56, 58, 28, "Colección"),        # 収集率 (porcentaje de la enciclopedia)
        (208, 28, 40, 20, "Máx."),            # Max (sin rectángulo en las plantillas)
    ],
    "STSH_004": [
        (0, 0, 32, 32, "NUE\nVO"),            # NEW (entrada nueva de la enciclopedia)
    ],
}
# Alto de la letra (de la línea de base al tope de las mayúsculas, en píxeles de
# la textura) por textura, como el original.
CAP = {"STFE_014": 11, "STFE_012": 15, "STSH_004": 11}


def parse(b):
    assert b[:4] == b"TTIX"
    out = {}
    for i in range(struct.unpack_from("<I", b, 8)[0]):
        e = 0x10 + 0x50 * i
        name = b[e:e + 8].rstrip(b"\0")
        name = (name[1:] if name and name[0] < 0x20 else name).decode("latin1")
        tex0 = struct.unpack_from("<Q", b, e + 0x40)[0]
        out[name] = dict(pix=struct.unpack_from("<I", b, e + 8)[0] + 0x80,
                         clut=struct.unpack_from("<I", b, e + 0x24)[0] + 0x80,
                         psm=(tex0 >> 20) & 63, w=1 << ((tex0 >> 26) & 15), h=1 << ((tex0 >> 30) & 15))
    return out


def _csm1(k):
    return (k & ~0x18) | ((k & 8) << 1) | ((k & 16) >> 1)


def palette(b, t):
    assert t["psm"] == 0x13, "solo texturas de 8 bits"
    raw = [tuple(b[t["clut"] + 4 * k:t["clut"] + 4 * k + 4]) for k in range(256)]
    return [raw[_csm1(k)] for k in range(256)]


def get(b, t, x, y):
    return b[t["pix"] + y * t["w"] + x]


def put(b, t, x, y, v):
    b[t["pix"] + y * t["w"] + x] = v


# ------------------------------------------------------------------ dibujo

def _glyph(font, ch):
    """(opacidades 22 × ancho, desplazamiento, avance) de un carácter."""
    if ch in sta_font.SPANISH:
        bm, r = sta_font.make_glyph(font, ch)
    else:
        bm, r = font.bitmap(ch)
    return bm, r[4], r[6]


def _line(font, text):
    """Opacidades (22 × ancho) de un renglón, con los avances de la fuente."""
    parts, x = [], 0
    for ch in text:
        bm, off, adv = _glyph(font, ch)
        parts.append((x + off, bm))
        x += adv
    w = max([x] + [px + len(bm[0]) for px, bm in parts])
    out = [[0] * w for _ in range(sta_font.H)]
    for px, bm in parts:
        for yy in range(sta_font.H):
            for xx, v in enumerate(bm[yy]):
                if 0 <= px + xx < w:
                    out[yy][px + xx] = max(out[yy][px + xx], v)
    return out


def _cap_box(font):
    """Filas del tope de las mayúsculas y de la línea de base en la celda."""
    bm, _o, _a = _glyph(font, "H")
    ink = [y for y in range(sta_font.H) if any(v > 60 for v in bm[y])]
    return min(ink), max(ink)


def render(font, text, w, h, cap):
    """Máscara (h × w, 0-255) del texto: cada renglón a la altura `cap` de
    mayúscula, centrado, estrechado a lo ancho si no entra (deja 1 px a la
    derecha y abajo para la sombra)."""
    from PIL import Image
    top, base = _cap_box(font)
    s = cap / (base - top + 1)
    lines = text.split("\n")
    line_h = round(sta_font.H * s)
    out = Image.new("L", (w, h), 0)
    total = line_h * len(lines)
    y0 = (h - 1 - total) // 2
    for n, ln in enumerate(lines):
        m = _line(font, ln)
        im = Image.new("L", (len(m[0]), sta_font.H))
        im.putdata([v for row in m for v in row])
        nw = max(1, round(im.width * s))
        nw = min(nw, w - 1)
        im = im.resize((nw, line_h), Image.LANCZOS)
        out.paste(im, ((w - 1 - nw) // 2, y0 + n * line_h))
    return out


def _nearest(pal, rgba, cache):
    if rgba not in cache:
        r, g, b, a = rgba
        cache[rgba] = min(range(256), key=lambda k: (pal[k][3] - a) ** 2 * 4 + (pal[k][0] - r) ** 2
                          + (pal[k][1] - g) ** 2 + (pal[k][2] - b) ** 2)
    return cache[rgba]


def _ink_colors(b, t, pal, u, v, w, h):
    """Color de la letra y de la sombra del original, dentro del rectángulo:
    el más claro y el más oscuro entre los píxeles casi opacos."""
    seen = [pal[get(b, t, x, y)] for y in range(v, v + h) for x in range(u, u + w)]
    solid = [p for p in seen if p[3] >= 0x70]
    fg = max(solid, key=lambda p: p[0] + p[1] + p[2])
    sh = min(solid, key=lambda p: p[0] + p[1] + p[2])
    return fg, sh


def draw(b, t, font, u, v, w, h, text, cap):
    pal = palette(b, t)
    fg, sh = _ink_colors(b, t, pal, u, v, w, h)
    mask = render(font, text, w, h, cap)
    m = mask.load()
    cache = {}
    for y in range(h):
        for x in range(w):
            a = m[x, y] / 255
            s = m[x - 1, y - 1] / 255 if x and y else 0
            # sombra debajo, letra encima (alfa del GS: 0x80 = opaco)
            alpha_s = s * sh[3]
            col = [0, 0, 0, 0]
            if alpha_s:
                col = [sh[0], sh[1], sh[2], alpha_s]
            if a:
                aa = a * fg[3] / 0x80
                base_a = col[3] / 0x80
                out_a = aa + base_a * (1 - aa)
                for k in range(3):
                    col[k] = (fg[k] * aa + col[k] * base_a * (1 - aa)) / out_a if out_a else 0
                col[3] = out_a * 0x80
            rgba = tuple(int(round(c)) for c in col)
            put(b, t, u + x, v + y, 0 if rgba[3] < 8 else _nearest(pal, rgba, cache))


def apply(body, font_table, font_tex):
    """Devuelve la entrada ENTRY con las palabras en español. La fuente es la
    original (las letras españolas se arman como en sta_font)."""
    b = bytearray(body)
    tex = parse(b)
    font = sta_font.Font(font_table, font_tex)
    for name, words in WORDS.items():
        t = tex[name]
        for u, v, w, h, text in words:
            draw(b, t, font, u, v, w, h, text, CAP[name])
    return bytes(b)


def preview(folder):
    import sta_text
    from stz import Stz
    from PIL import Image
    c = Stz(open(sta_text.STZ, "rb").read())
    old = c.body(ENTRY)
    new = apply(old, c.body(sta_font.FONT_TABLE), c.body(sta_font.FONT_TEX))
    os.makedirs(folder, exist_ok=True)
    for name in WORDS:
        for tag, b in (("original", old), ("es", new)):
            t = parse(b)[name]
            pal = palette(b, t)
            im = Image.new("RGBA", (t["w"], t["h"]))
            im.putdata([(lambda p: (p[0], p[1], p[2], min(255, p[3] * 2)))(pal[get(b, t, x, y)])
                        for y in range(t["h"]) for x in range(t["w"])])
            bg = Image.new("RGBA", im.size, (40, 40, 60, 255))
            bg.alpha_composite(im)
            bg = bg.resize((t["w"] * 4, t["h"] * 4), Image.NEAREST)
            p = os.path.join(folder, "%s_%s.png" % (name, tag))
            bg.convert("RGB").save(p)
            print(p)


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "preview":
        preview(sys.argv[2])
    else:
        print(__doc__)
        sys.exit(2)
