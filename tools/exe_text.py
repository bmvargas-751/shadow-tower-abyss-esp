#!/usr/bin/env python3
"""Textos del ejecutable de Shadow Tower Abyss (`SLPS_252.17`).

Casi todo el texto está en `STAZ.STZ` (sta_text.py). En el ejecutable quedan
los rótulos de algunos menús: la configuración de los botones (en japonés),
el porcentaje de enemigos eliminados (en japonés) y los rótulos que el original
ya trae en inglés (título, opciones, pausa, guardar y cargar, la enciclopedia y
la tienda). Ver TECH.md, «Ejecutable».

Cada texto ocupa un campo fijo dentro del ejecutable. El campo llega hasta el
próximo byte que no es 0, pero nunca hasta una dirección que el código use
(un `lui`/`addiu` o un puntero de 32 bits), porque esa puede ser otra cadena
(vacía) o un dato. Como mucho entran `campo - 1` bytes (con el `\\0`): es el
`max` de cada texto (T-4). Nada se mueve, como en el parche inglés.

Las claves son `exe#<dirección en hex>` (dirección virtual del juego).

    python3 tools/exe_text.py list        # campos, tamaños y referencias
    python3 tools/exe_text.py roundtrip   # escribir el original da el mismo ejecutable
"""
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sta_font  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCAL = os.path.join(os.path.dirname(ROOT), "local", "shadow-tower-abyss")
EXE = os.path.join(LOCAL, "iso-jp", "SLPS_252.17")
OUT = os.path.join(LOCAL, "build", "SLPS_252.17")
ISO_PATH = "/SLPS_252.17"         # en la ISO (ps2iso.py lo ubica por nombre)
ISO_EXE_LBA = 282                 # para leer el inglés del PPF
ENC = "cp932"
BASE = 0x100000 - 0x80            # dirección virtual - posición en el archivo (segmento de código y datos)
TEXT_END = 0x100000 + 0x101e80    # fin del segmento cargado desde el archivo

# Rótulos que ve el jugador, por pantalla (dirección virtual). Quedan fuera las
# cifras (4:3, 16:9, 16:9(LB)), «Dolby ProLogic II», los «----», «？？？？» y
# «Ｃ %d», «× %d», «%d ％» (sin palabras), y los nombres de archivo.
LABELS = {
    "título": [0x1f3380, 0x1f3390, 0x1fe718],
    "guardar y cargar": [0x1fcd00, 0x1fcd10, 0x1fcd20, 0x1fcd30, 0x1fcd40, 0x1fcd58, 0x1fcdc8,
                         0x1fd128, 0x1fd138, 0x1fd148, 0x1fd158, 0x1fd170, 0x1fd188, 0x1fd208,
                         0x1fcdf0],
    "opciones": [0x1fce08, 0x1fce18, 0x1fce30, 0x1fce50, 0x1fce60, 0x1fce68, 0x1fce88, 0x1fce90,
                 0x1fcea0, 0x1fceb0, 0x1fcec0, 0x1fced0, 0x1fcf00, 0x1fcf10, 0x1fd098, 0x1fd0a0,
                 0x1fd120],
    "botones": [0x1fcf20, 0x1fcf30, 0x1fcf40, 0x1fcf50, 0x1fcf68, 0x1fcf80,
                0x1fcf98, 0x1fcfa0, 0x1fcfb0, 0x1fcfc0, 0x1fcfc8, 0x1fcfd8, 0x1fcfe8, 0x1fcff0,
                0x1fcff8, 0x1fd000, 0x1fd010, 0x1fd020, 0x1fd030, 0x1fd040, 0x1fd050, 0x1fd058,
                0x1fd068, 0x1fd078, 0x1fd088, 0x1fd090],
    "enciclopedia": [0x1fd270, 0x1fd278, 0x1fd288, 0x1fd330, 0x1fd338, 0x1fd3a0, 0x1fd3d0],
    "estado": [0x1fd408, 0x1fd420],
    "pausa": [0x1fd610, 0x1fd618, 0x1fd628, 0x1fd638, 0x1fd648, 0x1fd650, 0x1fd660],
    "tienda": [0x1fd830, 0x1fd840, 0x1fd850, 0x1fd860,
               0x1fe7d0, 0x1fe7d8, 0x1fe7e0, 0x1fe7e8, 0x1fe7f0, 0x1fe7f8],
}
SCREEN = {a: s for s, v in LABELS.items() for a in v}


def s16(x):
    return x - 0x10000 if x & 0x8000 else x


def word(d, va):
    return struct.unpack_from("<I", d, va - BASE)[0]


def references(d, lo, hi):
    """Direcciones de [lo, hi) que usa el código (pares lui + addiu/ori/carga/guardado
    con el mismo registro) o que aparecen como puntero de 32 bits alineado.
    De más es seguro: solo achica campos."""
    refs = set()
    for va in range(0x100000, TEXT_END, 4):
        w = word(d, va)
        if lo <= w < hi:
            refs.add(w)                                   # puntero en los datos
        if w >> 26 != 0x0f:
            continue
        rt, up = (w >> 16) & 31, (w & 0xffff) << 16
        for q in range(va + 4, min(va + 80, TEXT_END), 4):
            v = word(d, q)
            op, rs, rt2 = v >> 26, (v >> 21) & 31, (v >> 16) & 31
            if rs == rt and op not in (0, 1, 2, 3, 4, 5, 0x0f):
                a = (up + (v & 0xffff if op == 0x0d else s16(v & 0xffff))) & 0xffffffff
                if lo <= a < hi:
                    refs.add(a)
            if op == 0 and ((v >> 11) & 31) == rt:
                break                                     # el registro se pisa
            if rt2 == rt and op not in (0, 1, 2, 3, 4, 5) and op not in (0x28, 0x29, 0x2b, 0x3f, 0x1f) \
                    and not (rs == rt and op in (0x09, 0x0d)):
                break
    return refs


def fields(d=None):
    """[(dirección, tamaño del campo con el \\0, texto original)] en orden."""
    if d is None:
        d = open(EXE, "rb").read()
    lo, hi = min(SCREEN), max(SCREEN) + 0x40
    refs = sorted(references(d, lo, hi))
    out = []
    for a in sorted(SCREEN):
        o = a - BASE
        end = d.index(b"\0", o)
        z = end
        while d[z] == 0:
            z += 1
        nxt = [r for r in refs if a < r]
        stop = min(z + BASE, nxt[0]) if nxt else z + BASE
        size = stop - a
        assert size > end - o, "exe#%06x: el campo no alcanza para el original" % a
        assert a in refs, "exe#%06x: el código no usa esta dirección" % a
        out.append((a, size, d[o:end].decode(ENC)))
    return out


def key(a):
    return "exe#%06x" % a


def items():
    """Textos para source.jsonl: {key, ja, max, note}."""
    return [{"key": key(a), "ja": t, "max": size - 1,
             "note": "ejecutable (%s), campo de %d bytes" % (SCREEN[a], size - 1)}
            for a, size, t in fields()]


def english(ppf):
    """{clave: inglés del PPF} de los rótulos que el parche cambia."""
    d = bytearray(open(EXE, "rb").read())
    p = open(ppf, "rb").read()
    assert p[:5] == b"PPF30"
    pos = 60 + (1024 if p[57] else 0)
    end = p.rfind(b"@BEGIN_FILE_ID.DIZ")
    end = end if end >= 0 else len(p)
    lo, hi = ISO_EXE_LBA * 2048, ISO_EXE_LBA * 2048 + len(d)
    while pos < end:
        off = struct.unpack_from("<Q", p, pos)[0]
        n = p[pos + 8]
        if lo <= off < hi:
            d[off - lo:off - lo + n] = p[pos + 9:pos + 9 + n][:hi - off]
        pos += 9 + n
    out = {}
    for a, _size, t in fields():
        o = a - BASE
        en = bytes(d[o:d.index(b"\0", o)]).decode(ENC, "replace")
        if en != t:
            out[key(a)] = en
    return out


def build(texts, font=True):
    """Ejecutable con los textos dados ({clave: texto}); lo que falta queda como
    el original. Con `font`, las letras españolas van con sus códigos prestados."""
    d = bytearray(open(EXE, "rb").read())
    errors = []
    for a, size, t in fields(bytes(d)):
        k = key(a)
        if k not in texts:
            continue
        s = texts[k]
        if font:
            bad = sta_font.missing(s)
            if bad:
                errors.append("%s: caracteres que la fuente no tiene: %s" % (k, "".join(sorted(set(bad)))))
                continue
            b = sta_font.encode(s)
        else:
            b = s.encode(ENC)
        if len(b) + 1 > size:
            errors.append("%s: %d bytes, el campo admite %d" % (k, len(b), size - 1))
            continue
        o = a - BASE
        d[o:o + size] = b + b"\0" * (size - len(b))
    if errors:
        raise SystemExit("ejecutable:\n  " + "\n  ".join(errors))
    return bytes(d)


def roundtrip():
    orig = open(EXE, "rb").read()
    same = build({key(a): t for a, _s, t in fields()}, font=False) == orig
    print("ejecutable, ida y vuelta:", "IDÉNTICO" if same else "DISTINTO")
    return same


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "list":
        for a, size, t in fields():
            print("%s  %-16s campo %2d  %s" % (key(a), SCREEN[a], size - 1, t.replace("\n", "|")))
    elif cmd == "roundtrip":
        sys.exit(0 if roundtrip() else 1)
    else:
        print(__doc__)
        sys.exit(2)
