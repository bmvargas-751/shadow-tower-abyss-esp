#!/usr/bin/env python3
"""Subtítulos en español de los videos (`TARGET/OPENING.PSS` y `PROLOGUE.PSS`).

Los dos son MPEG-2 (640×448, 30 cuadros por segundo) con audio aparte (TECH.md,
«Videos»). Cada uno se trata distinto:

- **Prólogo** (2075 cuadros): trae el texto japonés dibujado en la imagen, en 8
  bloques de dos renglones. Para cada bloque, mide cuadro por cuadro cuánto
  texto japonés se ve (su brillo contra el de alrededor) para seguir sus
  fundidos, hasta el bloque vecino; lo
  tapa rellenando una máscara del texto (los píxeles que están en la mitad de
  los cuadros del centro del bloque, porque el texto no se mueve) con los
  colores de alrededor, difuminados; y escribe el español donde estaba.
- **Apertura** (2265 cuadros): no trae texto, pero tiene una narración en
  japonés. No hay transcripción, así que el español sale de los subtítulos del
  inglés fan [DECISIONS 2026-11-28]; va abajo, en la franja negra, con los
  tiempos de esos subtítulos y fundidos cortos.

El español va con la fuente del juego (sta_font, con las letras españolas)
[DECISIONS 2026-11-28]. El video se vuelve a codificar con ffmpeg (MPEG-2, sin
cuadros B) y se mete en los mismos paquetes del PSS: el audio (0xBD) y los
paquetes de sistema quedan idénticos, y cada paquete de video conserva su largo
y su cabecera de 10 bytes; solo cambian los datos y el PTS/DTS de los cuadros.
Un paquete de video no adelanta más de LEAD cuadros al original (si se
adelantaría, va de relleno 0xBE), para que el video llegue al mismo ritmo que el
audio. Lo que sobra al final también va de relleno. El archivo conserva su
tamaño.

    python3 tools/pss_sub.py build ISO_ORIGINAL VIDEO SALIDA.PSS     # VIDEO: OPENING o PROLOGUE
    python3 tools/pss_sub.py preview ISO_ORIGINAL VIDEO CARPETA      # un cuadro de cada bloque
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

W, H, FPS = 640, 448, 30
LEAD = 2               # cuadros que el video nuevo puede adelantarse al original
QUALITY = 2            # cuantizador fijo de ffmpeg (2 = casi sin pérdida); los originales van a 6 Mb/s

# Bloques: (primer cuadro, último cuadro, español).
# Prólogo: los cuadros salen de la medida del texto japonés (umbral de 60
# píxeles); los fundidos se buscan hasta el bloque vecino (windows).
# Apertura: los tiempos de los subtítulos del inglés fan, ajustados por el
# usuario contra la voz en las pruebas 8 a 13 (2026-11-28): 1,5–10,6 s,
# 11,5–19 s, 20,3–25 s y 25–34,7 s.
VIDEOS = {
    "PROLOGUE": dict(
        path="/TARGET/PROLOGUE.PSS", frames=2075, mode="cover",
        subs=[
            (88, 232, "Antaño, en lo profundo de aquel bosque,\nexistía un reino"),
            (293, 438, "El rey que gobernaba a su pueblo\ncon poderes y ritos misteriosos"),
            (459, 590, "llevaba a su lado, según se dice,\nuna \"lanza\" aberrante"),
            (648, 792, "Con el poder de la lanza,\nel rey sometió a los reinos vecinos"),
            (820, 935, "y le dio a su reino\nuna prosperidad sin precedentes,"),
            (949, 1173, "pero nadie supo de los ritos\nque en su sombra se celebraban en secreto"),
            (1259, 1547, "Hoy, al cabo de los siglos, cuando incluso en las leyendas\n"
                         "el nombre del Rey de la Lanza se ha vuelto difuso,"),
            (1560, 1950, "un hombre guiado por un anciano\nllegó a aquella tierra"),
        ]),
    "OPENING": dict(
        path="/TARGET/OPENING.PSS", frames=2265, mode="overlay", center_y=418,
        subs=[
            (45, 317, "En lo profundo del bosque sombrío, un viejo guía llevó\n"
                      "a un joven hasta un pequeño santuario abandonado y en ruinas"),
            (345, 569, "Desde la entrada abismal, entre las ruinas desmoronadas\n"
                       "del santuario, brotaba la oscuridad"),
            (609, 749, "El viejo guía hizo una reverencia\nmientras el joven entraba con cautela"),
            (750, 1041, "Y una vez más, la oscuridad\nse tragó a un ser humano"),
        ]),
}
ISO_PATHS = {name: v["path"] for name, v in VIDEOS.items()}
FADE_OVERLAY = 6       # apertura: fundido de entrada y salida, en cuadros
TEXT_BAND = (300, 440)            # prólogo: filas donde va el texto japonés
FAINT_MIN = 8                     # prólogo: píxeles grises que todavía cuentan como texto
MARGIN = 6                        # prólogo: cuadros de más que se tapan a cada lado del tramo
RAMP = 15                         # prólogo: cuadros del fundido del español
LINE_H = 30                       # renglón del español, en píxeles
WHITE = (235, 235, 235)


def read_pss(iso, name):
    with open(iso, "rb") as f:
        _pos, lba, size = ps2iso.iso_records(f)[VIDEOS[name]["path"]]
        f.seek(lba * ps2iso.S)
        return f.read(size)


def frames(pss):
    """Cuadros RGB (PIL) del video original."""
    import threading
    from PIL import Image
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", "-", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def feed():
        try:
            p.stdin.write(pss)
            p.stdin.close()
        except BrokenPipeError:
            pass
    threading.Thread(target=feed, daemon=True).start()
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


def block_of(subs, n, fade):
    for k, (a, b, _t) in enumerate(subs):
        if a - fade <= n <= b + fade:
            return k
    return None


def windows(subs, total):
    """Prólogo: cuadros donde se busca cada bloque, hasta el anterior y el
    siguiente: los fundidos del japonés son largos y un bloque se funde con el
    siguiente (se ven los dos a la vez)."""
    out = []
    for k, (a, b, _t) in enumerate(subs):
        lo = subs[k - 1][0] if k else max(0, a - 90)
        hi = subs[k + 1][1] if k + 1 < len(subs) else min(total - 1, b + 120)
        out.append((lo, hi))
    return out


def faint(im):
    """Máscara (L) de los píxeles grises algo claros: el texto japonés, también
    cuando está casi apagado en un fundido."""
    from PIL import ImageChops
    _h, s, v = im.convert("HSV").split()
    return ImageChops.multiply(v.point(lambda x: 255 if x > 40 else 0), s.point(lambda x: 255 if x < 60 else 0))


def analyze(pss, subs, total):
    """Prólogo, por bloque: la máscara del japonés, el tramo donde se ve y la
    opacidad del español en cada cuadro del tramo.

    La máscara son los píxeles blancos en al menos la mitad de los cuadros del
    centro del bloque (uno de cada 3): el texto no se mueve y la lanza sí. El
    tramo va desde el bloque hacia atrás y hacia adelante mientras queden más
    de FAINT_MIN píxeles grises (umbral bajo) en la parte de la máscara que no
    es de los bloques vecinos: así cubre los fundidos enteros, hasta que el texto
    se apaga."""
    from PIL import ImageChops, ImageFilter
    y0, y1 = TEXT_BAND
    acc, cnt = {}, {}
    for n, im in enumerate(frames(pss)):
        k = block_of(subs, n, 0)
        if k is None:
            continue
        a, b, _t = subs[k]
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
        core[k] = m.filter(ImageFilter.MaxFilter(3))
        hole = m.filter(ImageFilter.MaxFilter(11))
        full = hole.filter(ImageFilter.GaussianBlur(2))
        masks[k] = (full, m.getbbox(), hole)
    # para medir, solo los píxeles de cada bloque que no son de sus vecinos
    # (en los fundidos cruzados se ven los dos)
    excl = {}
    for k in core:
        e = core[k]
        for j in (k - 1, k + 1):
            if j in core:
                e = ImageChops.subtract(e, core[j].filter(ImageFilter.MaxFilter(5)))
        excl[k] = e
    win = windows(subs, total)
    seen = {}
    for n, im in enumerate(frames(pss)):
        f = None
        for k, (lo, hi) in enumerate(win):
            if lo <= n <= hi:
                if f is None:
                    f = faint(im)
                seen[(n, k)] = ImageChops.multiply(f, excl[k]).histogram()[255]
    spans = []
    for k, (a, b, _t) in enumerate(subs):
        lo, hi = win[k]
        a2 = a
        while a2 - 1 >= lo and seen.get((a2 - 1, k), 0) > FAINT_MIN:
            a2 -= 1
        b2 = b
        while b2 + 1 <= hi and seen.get((b2 + 1, k), 0) > FAINT_MIN:
            b2 += 1
        a2, b2 = max(lo, a2 - MARGIN), min(hi, b2 + MARGIN)
        # opacidad del español: entera mientras el japonés se ve claro (a..b,
        # la medida por umbral), con un fundido de RAMP cuadros a cada lado. La
        # medida del brillo cuadro a cuadro se confundía con las cuchillas de
        # la lanza y dejaba el español gris (prueba del 2026-11-28).
        alpha = {n: max(0.0, min(1.0, (n - (a - RAMP)) / RAMP, ((b + RAMP) - n) / RAMP))
                 for n in range(a2, b2 + 1)}
        spans.append((a2, b2, alpha))
    return spans, masks


def text_layer(font, text, center_y):
    """(máscara del español y de su sombra, centrada en x = W/2 y en `center_y`)."""
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


def _text(im, layer, p):
    from PIL import Image
    text, shadow = layer
    out = Image.composite(Image.new("RGB", (W, H)), im, shadow.point(lambda x: int(x * p * 0.8)))
    return Image.composite(Image.new("RGB", (W, H), WHITE), out, text.point(lambda x: int(x * p)))


def cover(im, on, masks, layers):
    """Prólogo: tapa el japonés de los bloques que se ven (en los fundidos
    cruzados, dos) y escribe encima el español de cada uno, con su opacidad.
    [(bloque, opacidad)]"""
    from PIL import Image
    for k, _p in on:
        mask, _box, hole = masks[k]
        im = Image.composite(_fill(im, hole), im, mask)   # tapado entero en todo el tramo
    for k, p in on:
        im = _text(im, layers[k], p)
    return im


def font():
    c = Stz(open(sta_text.STZ, "rb").read())
    return sta_font.Font(c.body(sta_font.FONT_TABLE), c.body(sta_font.FONT_TEX))


def render(pss, name, only=None):
    """Genera los cuadros traducidos (todos, o solo los de `only`)."""
    v = VIDEOS[name]
    subs = v["subs"]
    f = font()
    if v["mode"] == "cover":
        spans, masks = analyze(pss, subs, v["frames"])
        layers = {}
        for k, (_a, _b, t) in enumerate(subs):
            box = masks[k][1]
            layers[k] = text_layer(f, t, (box[1] + box[3]) / 2 if box else 380)
    else:
        layers = {k: text_layer(f, t, v["center_y"]) for k, (_a, _b, t) in enumerate(subs)}
    for n, im in enumerate(frames(pss)):
        if only is not None and n not in only:
            continue
        if v["mode"] == "cover":
            on = []
            for k, (a2, b2, alpha) in enumerate(spans):
                if a2 <= n <= b2:
                    on.append((k, alpha[n]))
            im = cover(im, on, masks, layers)
        else:
            k = block_of(subs, n, 0)
            if k is not None:
                a, b, _t = subs[k]
                p = min(1.0, (n - a + 1) / FADE_OVERLAY, (b - n + 1) / FADE_OVERLAY)
                im = _text(im, layers[k], p)
        yield n, im


def encode(pss, name):
    """Video MPEG-2 nuevo (elemental), sin cuadros B."""
    import threading
    p = subprocess.Popen([
        "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "%dx%d" % (W, H),
        "-r", str(FPS), "-i", "-", "-c:v", "mpeg2video", "-pix_fmt", "yuv420p", "-q:v", str(QUALITY),
        "-maxrate", "9000k", "-bufsize", "1835k", "-g", "18", "-bf", "0", "-flags", "+cgop",
        "-sc_threshold", "1000000000", "-aspect", "%d:%d" % (W, H), "-f", "mpeg2video", "-"],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out = []
    t = threading.Thread(target=lambda: out.append(p.stdout.read()))
    t.start()
    n = -1
    for n, im in render(pss, name):
        p.stdin.write(im.tobytes())
    p.stdin.close()
    t.join()
    assert p.wait() == 0 and n + 1 == VIDEOS[name]["frames"], "ffmpeg falló o faltan cuadros (%d)" % (n + 1)
    return out[0]


def _ts(prefix, v):
    return bytes([(prefix << 4) | (((v >> 30) & 7) << 1) | 1, (v >> 22) & 0xff,
                  (((v >> 15) & 0x7f) << 1) | 1, (v >> 7) & 0xff, ((v & 0x7f) << 1) | 1])


def _pts(b):
    return (((b[0] >> 1) & 7) << 30) | (b[1] << 22) | ((b[2] >> 1) << 15) | (b[3] << 7) | (b[4] >> 1)


def _padding(n):
    assert n >= 6
    return b"\0\0\1\xbe" + struct.pack(">H", n - 6) + b"\xff" * (n - 6)


def mux(pss, es, frames_n):
    """PSS nuevo: los paquetes del original, con el video `es` en lugar del viejo.
    El primer cuadro conserva el PTS del original (el audio empieza igual)."""
    pics = []
    i = es.find(b"\0\0\1\0")
    while i >= 0:
        pics.append(i)
        i = es.find(b"\0\0\1\0", i + 4)
    assert len(pics) == frames_n, "el video nuevo tiene %d cuadros" % len(pics)
    out = bytearray()
    d = pss
    i = 0
    pos = 0             # posición en el video nuevo
    nxt = 0             # próximo cuadro nuevo que empieza
    orig = 0            # cuadros del original que ya empezaron
    pts0 = None
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
            if pts0 is None:
                pts0 = _pts(d[i + 9:i + 14])
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
            v = pts0 + 3000 * starts[0]
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


def build(iso, name, out):
    pss = read_pss(iso, name)
    es = encode(pss, name)
    new = mux(pss, es, VIDEOS[name]["frames"])
    with open(out, "wb") as f:
        f.write(new)
    print("video: %s (%d bytes, video %d bytes)" % (out, len(new), len(es)))
    return out


def preview(iso, name, folder):
    pss = read_pss(iso, name)
    os.makedirs(folder, exist_ok=True)
    subs = VIDEOS[name]["subs"]
    want = {round((a + b) / 2) for a, b, _t in subs} | {subs[0][0] + 2}
    for n, im in render(pss, name, only=want):
        p = os.path.join(folder, "%s_%04d.png" % (name.lower(), n))
        im.save(p)
        print(p)


if __name__ == "__main__":
    if len(sys.argv) == 5 and sys.argv[1] == "build":
        build(sys.argv[2], sys.argv[3], sys.argv[4])
    elif len(sys.argv) == 5 and sys.argv[1] == "preview":
        preview(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print(__doc__)
        sys.exit(2)
