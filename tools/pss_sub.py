#!/usr/bin/env python3
"""Subtítulos en español del video del prólogo (`TARGET/PROLOGUE.PSS`).

El video (MPEG-2, 640×448, 30 cuadros por segundo, 2075 cuadros) trae el texto
japonés dibujado en la imagen, en 8 bloques de dos renglones (TECH.md, «Otro
texto»). Para cada bloque:

1. Mide, cuadro por cuadro, cuánto texto japonés se ve (píxeles blancos sin
   color, fuera de la columna de la lanza): así sigue sus fundidos.
2. Tapa el japonés: rellena una máscara hecha con los píxeles del texto
   (los que están en la mitad de los cuadros del centro del bloque, porque el
   texto no se mueve) con los colores de alrededor, difuminados.
3. Escribe el español encima, centrado donde estaba el japonés, con la fuente
   del juego (sta_font, con las letras españolas) [DECISIONS 2026-11-28].

El video se vuelve a codificar con ffmpeg (MPEG-2, sin cuadros B) y se mete en
los mismos paquetes del PSS: el audio (0xBD) y los paquetes de sistema quedan
idénticos, y cada paquete de video conserva su largo y su cabecera de 10 bytes;
solo cambian los datos y el PTS/DTS de los cuadros. Un paquete de video no
adelanta más de LEAD cuadros al original (si se adelantaría, va de relleno
0xBE), para que el video llegue al mismo ritmo que el audio. Lo que sobra al
final también va de relleno. El archivo conserva su tamaño.

    python3 tools/pss_sub.py build ISO_ORIGINAL SALIDA.PSS
    python3 tools/pss_sub.py preview ISO_ORIGINAL CARPETA   # un cuadro de cada bloque
"""
import os
import struct
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ps2iso  # noqa: E402
import sta_font  # noqa: E402
import sta_text  # noqa: E402
import sta_tex  # noqa: E402
from stz import Stz  # noqa: E402

ISO_PATH = "/TARGET/PROLOGUE.PSS"
W, H, FPS = 640, 448, 30
FRAMES = 2075
PTS0 = 3986            # PTS del primer cuadro (el del original; el audio empieza igual)
LEAD = 2               # cuadros que el video nuevo puede adelantarse al original
QUALITY = 2            # cuantizador fijo de ffmpeg (2 = casi sin pérdida); el original va a 6 Mb/s

# Bloques: (primer cuadro, último cuadro con texto, español). Los cuadros salen
# de la medida del texto japonés (umbral de 60 píxeles); se amplían FADE cuadros
# a cada lado para los fundidos. El japonés de cada bloque, en DECISIONS.
FADE = 20
SUBS = [
    (88, 232, "Antaño, en lo profundo de aquel bosque,\nexistía un reino"),
    (293, 438, "El rey que gobernaba a su pueblo\ncon poderes y ritos misteriosos"),
    (459, 590, "llevaba a su lado, según se dice,\nuna \"lanza\" aberrante"),
    (648, 792, "Con el poder de la lanza,\nel rey sometió a los reinos vecinos"),
    (820, 935, "y le dio a su reino\nuna prosperidad sin precedentes,"),
    (949, 1173, "pero nadie supo de los ritos\nque en su sombra se celebraban en secreto"),
    (1259, 1547, "Hoy, al cabo de los siglos, cuando incluso en las leyendas\nel nombre del Rey de la Lanza se ha vuelto difuso,"),
    (1560, 1950, "un hombre guiado por un anciano\nllegó a aquella tierra"),
]
TEXT_BAND = (300, 440)            # filas donde va el texto japonés
SPEAR = (290, 360)                # columna de la lanza (no cuenta al medir)
LINE_H = 30                       # renglón del español, en píxeles
WHITE = (235, 235, 235)


def read_pss(iso):
    with open(iso, "rb") as f:
        _pos, lba, size = ps2iso.iso_records(f)[ISO_PATH]
        f.seek(lba * ps2iso.S)
        return f.read(size)


def frames(pss):
    """Cuadros RGB (PIL) del video original."""
    from PIL import Image
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", "-", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    import threading
    threading.Thread(target=lambda: (p.stdin.write(pss), p.stdin.close()), daemon=True).start()
    while True:
        buf = p.stdout.read(W * H * 3)
        if len(buf) < W * H * 3:
            break
        yield Image.frombytes("RGB", (W, H), buf)
    p.wait()


def white(im):
    """Máscara (L) de los píxeles blancos sin color: el texto japonés."""
    from PIL import ImageChops
    _h, s, v = im.convert("HSV").split()
    return ImageChops.multiply(v.point(lambda x: 255 if x > 90 else 0), s.point(lambda x: 255 if x < 60 else 0))


def amount(mask):
    y0, y1 = TEXT_BAND
    return mask.crop((100, y0, SPEAR[0], y1)).histogram()[255] + mask.crop((SPEAR[1], y0, 540, y1)).histogram()[255]


def block_of(n):
    for k, (a, b, _t) in enumerate(SUBS):
        if a - FADE <= n <= b + FADE:
            return k
    return None


def analyze(pss):
    """Por bloque: la máscara del japonés y cuánto se ve en cada cuadro (0 a 1).

    La máscara son los píxeles blancos en al menos la mitad de los cuadros del
    centro del bloque (uno de cada 3): el texto no se mueve y la lanza sí. Lo que
    se ve de él en cada cuadro se mide dentro de esa máscara."""
    from PIL import ImageChops, ImageFilter
    y0, y1 = TEXT_BAND
    acc, cnt = {}, {}
    for n, im in enumerate(frames(pss)):
        k = block_of(n)
        if k is None:
            continue
        a, b, _t = SUBS[k]
        if not (a + (b - a) * 0.15 <= n <= a + (b - a) * 0.85) or (n - a) % 3:
            continue
        m = white(im).point(lambda x: 1 if x else 0)
        acc[k] = ImageChops.add(acc[k], m) if k in acc else m
        cnt[k] = cnt.get(k, 0) + 1
    core, masks = {}, {}
    for k in acc:
        half = cnt[k] // 2
        m = acc[k].point(lambda x: 255 if x >= half else 0)
        band = m.crop((0, y0, W, y1))
        m = m.point(lambda x: 0)
        m.paste(band, (0, y0))
        core[k] = m
        hole = m.filter(ImageFilter.MaxFilter(11))
        full = hole.filter(ImageFilter.GaussianBlur(2))
        masks[k] = (full, m.getbbox(), hole)
    amounts, peak = {}, [1] * len(SUBS)
    for n, im in enumerate(frames(pss)):
        k = block_of(n)
        if k is None:
            continue
        amounts[n] = ImageChops.multiply(white(im), core[k]).histogram()[255]
        peak[k] = max(peak[k], amounts[n])
    return amounts, peak, masks


def text_layer(font, text, center_y):
    """(capa RGBA del español, centrada en x = W/2 y en `center_y`)."""
    from PIL import Image, ImageFilter
    lines = text.split("\n")
    layer = Image.new("L", (W, H), 0)
    top = round(center_y - LINE_H * len(lines) / 2)
    for i, ln in enumerate(lines):
        m = sta_tex._line(font, ln)
        im = Image.new("L", (len(m[0]), sta_font.H))
        im.putdata([v for row in m for v in row])
        x = (W - im.width) // 2
        assert im.width <= W - 40, "renglón demasiado ancho: %r (%d)" % (ln, im.width)
        layer.paste(im, (x, top + i * LINE_H + (LINE_H - sta_font.H) // 2))
    shadow = layer.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(1.5))
    return layer, shadow


FILL_TOP = 290          # el relleno se calcula solo desde esta fila
FILL_BLUR = 10


def _fill(im, hole):
    """El cuadro con el hueco relleno con los colores de alrededor (convolución
    normalizada: desenfoque de lo que no es hueco, dividido por su peso)."""
    from PIL import Image, ImageChops, ImageFilter, ImageMath
    crop = im.crop((0, FILL_TOP, W, H))
    hole = hole.crop((0, FILL_TOP, W, H))
    keep = ImageChops.invert(hole)
    num = Image.composite(crop, Image.new("RGB", crop.size), keep).filter(ImageFilter.GaussianBlur(FILL_BLUR))
    den = keep.filter(ImageFilter.GaussianBlur(FILL_BLUR))
    bands = [ImageMath.eval("convert(a * 255 / (b + 1), 'L')", a=c, b=den) for c in num.split()]
    out = im.copy()
    out.paste(Image.merge("RGB", bands), (0, FILL_TOP))
    return out


def compose(im, k, amount_n, peak, masks, layers):
    """Cuadro con el japonés tapado y el español encima, según cuánto se ve."""
    from PIL import Image
    p = max(0.0, min(1.0, amount_n / max(1, peak[k]) * 1.15))
    if p <= 0.01:
        return im
    mask, _box, hole = masks[k]
    cover = min(1.0, p * 3)
    out = Image.composite(_fill(im, hole), im, mask.point(lambda x: int(x * cover)))
    black = Image.new("RGB", (W, H), (0, 0, 0))
    text, shadow = layers[k]
    out = Image.composite(black, out, shadow.point(lambda x: int(x * p * 0.8)))
    out = Image.composite(Image.new("RGB", (W, H), WHITE), out, text.point(lambda x: int(x * p)))
    return out


def font():
    c = Stz(open(sta_text.STZ, "rb").read())
    return sta_font.Font(c.body(sta_font.FONT_TABLE), c.body(sta_font.FONT_TEX))


def render(pss, out_raw=None, only=None):
    """Genera los cuadros traducidos (para ffmpeg, o solo los de `only`)."""
    amounts, peak, masks = analyze(pss)
    f = font()
    layers = {}
    for k, (_a, _b, t) in enumerate(SUBS):
        box = masks[k][1]
        cy = (box[1] + box[3]) / 2 if box else 380
        layers[k] = text_layer(f, t, cy)
    for n, im in enumerate(frames(pss)):
        k = block_of(n)
        if k is not None:
            im = compose(im, k, amounts[n], peak, masks, layers)
        if only is not None:
            if n in only:
                yield n, im
        else:
            yield n, im


def encode(pss):
    """Video MPEG-2 nuevo (elemental), sin cuadros B."""
    p = subprocess.Popen([
        "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "%dx%d" % (W, H),
        "-r", str(FPS), "-i", "-", "-c:v", "mpeg2video", "-pix_fmt", "yuv420p", "-q:v", str(QUALITY),
        "-maxrate", "9000k", "-bufsize", "1835k", "-g", "18", "-bf", "0", "-flags", "+cgop",
        "-sc_threshold", "1000000000", "-aspect", "%d:%d" % (W, H), "-f", "mpeg2video", "-"],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    import threading
    out = []
    t = threading.Thread(target=lambda: out.append(p.stdout.read()))
    t.start()
    n = 0
    for n, im in render(pss):
        p.stdin.write(im.tobytes())
    p.stdin.close()
    t.join()
    assert p.wait() == 0 and n + 1 == FRAMES, "ffmpeg falló o faltan cuadros (%d)" % (n + 1)
    return out[0]


def _ts(prefix, v):
    return bytes([(prefix << 4) | (((v >> 30) & 7) << 1) | 1, (v >> 22) & 0xff,
                  (((v >> 15) & 0x7f) << 1) | 1, (v >> 7) & 0xff, ((v & 0x7f) << 1) | 1])


def _padding(n):
    assert n >= 6
    return b"\0\0\1\xbe" + struct.pack(">H", n - 6) + b"\xff" * (n - 6)


def mux(pss, es):
    """PSS nuevo: los paquetes del original, con el video `es` en lugar del viejo."""
    pics = []
    i = es.find(b"\0\0\1\0")
    while i >= 0:
        pics.append(i)
        i = es.find(b"\0\0\1\0", i + 4)
    assert len(pics) == FRAMES, "el video nuevo tiene %d cuadros" % len(pics)
    out = bytearray()
    d = pss
    i = 0
    pos = 0             # posición en el video nuevo
    nxt = 0             # próximo cuadro nuevo que empieza
    orig = 0            # cuadros del original que ya empezaron
    while i < len(d):
        assert d[i:i + 3] == b"\0\0\1"
        sid = d[i + 3]
        if sid == 0xba:
            n = 14 + (d[i + 13] & 7)
            out += d[i:i + n]
            i += n
            continue
        if sid == 0xb9:
            out += d[i:i + 4]
            i += 4
            continue
        L = struct.unpack_from(">H", d, i + 4)[0]
        if sid != 0xe0:
            out += d[i:i + 6 + L]
            i += 6 + L
            continue
        hl = d[i + 8]
        if d[i + 7] & 0x80:
            orig += 1
        cap = L - 3 - hl
        total = 6 + L
        chunk_end = min(pos + cap, len(es))
        starts = [k for k in range(nxt, len(pics)) if pics[k] < chunk_end]
        if pos >= len(es) or (starts and starts[0] >= orig + LEAD):
            out += _padding(total)
            i += total
            continue
        payload = es[pos:chunk_end]
        flags = bytearray(d[i + 6:i + 9])
        head = b""
        if starts:
            v = PTS0 + 3000 * starts[0]
            head = _ts(3, v) + _ts(1, v)
            flags[1] = 0xc0
            nxt = starts[-1] + 1
        else:
            flags[1] = 0x00
        flags[2] = hl
        head += b"\xff" * (hl - len(head))
        size = 3 + hl + len(payload)
        pkt = b"\0\0\1\xe0" + struct.pack(">H", size) + bytes(flags) + head + payload
        rest = total - len(pkt)
        if rest:
            if rest < 6:     # no entra un relleno: más bytes de relleno en la cabecera
                flags[2] = hl + rest
                pkt = b"\0\0\1\xe0" + struct.pack(">H", size + rest) + bytes(flags) + head + b"\xff" * rest + payload
            else:
                pkt += _padding(rest)
        assert len(pkt) == total
        out += pkt
        pos = chunk_end
        i += total
    assert pos >= len(es), "el video nuevo no entra: faltan %d bytes" % (len(es) - pos)
    assert len(out) == len(d)
    return bytes(out)


def build(iso, out):
    pss = read_pss(iso)
    es = encode(pss)
    new = mux(pss, es)
    with open(out, "wb") as f:
        f.write(new)
    print("video: %s (%d bytes, video %d bytes)" % (out, len(new), len(es)))
    return out


def preview(iso, folder):
    pss = read_pss(iso)
    os.makedirs(folder, exist_ok=True)
    want = {round((a + b) / 2) for a, b, _t in SUBS} | {SUBS[0][0] + 4}
    for n, im in render(pss, only=want):
        p = os.path.join(folder, "prologo_%04d.png" % n)
        im.save(p)
        print(p)


if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[1] == "build":
        build(sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 4 and sys.argv[1] == "preview":
        preview(sys.argv[2], sys.argv[3])
    else:
        print(__doc__)
        sys.exit(2)
