#!/usr/bin/env python3
"""Adaptador de texto de Shadow Tower Abyss (PS2, SLPS-25217).

Todo el texto del juego está en `TARGET/STAZ.STZ`, en tablas `STA `:

- 4 tablas sueltas (entradas 15 a 18 del contenedor): criaturas, objetos,
  lugares y ayudas del menú.
- 34 tablas dentro del bloque `MSGa` de cada mapa (`STAM`, entradas 2248+).

Comandos (desde la raíz del repo):

    python3 tools/sta_text.py export      # original -> source.jsonl (+ ref_en.jsonl)
    python3 tools/sta_text.py import      # translation/ -> build/STAZ.STZ
    python3 tools/sta_text.py roundtrip   # export + import sin cambios == original

Los archivos del juego y lo que se genera van en ../shadow-tower-abyss-esp-local/.
"""
import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stz import Stz  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCAL = os.path.join(os.path.dirname(ROOT), "shadow-tower-abyss-esp-local")
STZ = os.path.join(LOCAL, "iso-jp", "TARGET", "STAZ.STZ")
PPF = "/mnt/d/Emulation/roms/ps2/Shadow Tower Abyss/STATest0.3.ppf"
ISO_STZ_LBA = 525217  # sector de STAZ.STZ en la ISO japonesa
SOURCE = os.path.join(LOCAL, "source.jsonl")
REF_EN = os.path.join(LOCAL, "ref_en.jsonl")
OUT = os.path.join(LOCAL, "build", "STAZ.STZ")
TRANSLATION = os.path.join(ROOT, "translation")

ENC = "cp932"
SECTOR = 0x800

# Tablas sueltas: entrada del contenedor -> nombre del archivo en las claves
LOOSE = {15: "sys/criaturas", 16: "sys/objetos", 17: "sys/lugares", 18: "sys/menu"}
# Campos de los registros de 12 bytes (id, cadena 1, cadena 2)
FIELDS12 = ("nombre", "desc")


# ---------------------------------------------------------------- contenedor

def entries(stz):
    """Tabla del contenedor: [(tamaño, tamaño2, tamaño con cabecera, sector)]."""
    assert stz[:4] == b"STAZ"
    n = struct.unpack_from("<I", stz, 8)[0]
    out = []
    for i in range(n):
        mg, a, b, c, _h1, _h2, sec, _x = struct.unpack_from("<4sIIIIIII", stz, 16 + i * 32)
        assert mg == b"STZ0"
        out.append((a, b, c, sec))
    return out


def find_tables(stz):
    """Ubica las 38 tablas STA: [(archivo, inicio absoluto de STA, tipo)]."""
    found = []
    for i, (size, _b, _c, sec) in enumerate(entries(stz)):
        base = sec * SECTOR
        if i in LOOSE:
            assert stz[base:base + 4] == b"STA "
            found.append((LOOSE[i], base, "suelta"))
            continue
        if stz[base:base + 4] != b"STAM":
            continue
        body = stz[base:base + size]
        k = body.find(b"MSGa")
        while k >= 0:
            if body[k + 0x20:k + 0x24] == b"STA ":
                found.append(("mapa/%04d" % i, base + k + 0x20, "msga"))
            k = body.find(b"MSGa", k + 4)
    return found


def parse_table(buf, o):
    """Lee una tabla STA en buf[o:]. Devuelve (cuenta, tamaño de registro, registros)."""
    assert buf[o:o + 4] == b"STA "
    n32 = struct.unpack_from("<I", buf, o + 4)[0]
    n16 = struct.unpack_from("<H", buf, o + 6)[0]
    for cnt in (n32, n16):
        for rs in (8, 12):
            if 0 < cnt < 5000 and struct.unpack_from("<I", buf, o + 20)[0] == 16 + cnt * rs:
                recs = [struct.unpack_from("<%dI" % (rs // 4), buf, o + 16 + r * rs) for r in range(cnt)]
                return cnt, rs, recs
    if n16 == 0 and buf[o + 8:o + 16] == bytes(8):  # tabla vacía de un mapa (solo cabecera)
        return 0, 8, []
    raise ValueError("tabla STA no reconocida en %#x" % o)


def cstr(buf, o):
    return buf[o:buf.index(b"\0", o)]


def table_keys(name, rs, recs):
    """Claves de cada cadena, en orden de la tabla: [(clave, nº de registro, campo)]."""
    keys, seen = [], {}
    for r, rec in enumerate(recs):
        rid = rec[0]
        seen[rid] = seen.get(rid, 0) + 1
        base = "%s#%04d" % (name, rid) + ("" if seen[rid] == 1 else "~%d" % seen[rid])
        for f in range(1, len(rec)):
            if rec[f] == 0:
                continue
            keys.append((base if rs == 8 else "%s/%s" % (base, FIELDS12[f - 1]), r, f))
    return keys


def read_texts(buf, tables):
    """[(clave, texto, nota)] de todas las tablas, en el orden del juego."""
    out = []
    for name, o, kind in tables:
        _cnt, rs, recs = parse_table(buf, o)
        for key, r, f in table_keys(name, rs, recs):
            raw = cstr(buf, o + recs[r][f])
            out.append((key, raw.decode(ENC), kind))
    return out


# ---------------------------------------------------------------- PPF (inglés fan)

def apply_ppf_to_stz(stz):
    """Aplica en memoria los cambios del PPF que caen dentro de STAZ.STZ."""
    p = open(PPF, "rb").read()
    assert p[:5] == b"PPF30"
    pos = 60 + (1024 if p[57] else 0)
    end = len(p)
    k = p.rfind(b"@BEGIN_FILE_ID.DIZ")
    if k >= 0:
        end = k
    buf = bytearray(stz)
    lo, hi = ISO_STZ_LBA * SECTOR, ISO_STZ_LBA * SECTOR + len(stz)
    while pos < end:
        off = struct.unpack_from("<Q", p, pos)[0]
        n = p[pos + 8]
        data = p[pos + 9:pos + 9 + n]
        pos += 9 + n
        if lo <= off < hi:
            buf[off - lo:off - lo + n] = data
    return bytes(buf)


# ---------------------------------------------------------------- export

def export():
    stz = open(STZ, "rb").read()
    tables = find_tables(stz)
    rows = read_texts(stz, tables)
    os.makedirs(LOCAL, exist_ok=True)
    with open(SOURCE, "w", encoding="utf-8") as f:
        for key, text, kind in rows:
            d = {"key": key, "en": text}
            if kind == "suelta":
                d["note"] = "tabla de sistema"
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
    print("source: %d textos en %d tablas -> %s" % (len(rows), len(tables), SOURCE))
    if os.path.exists(PPF):
        en = apply_ppf_to_stz(stz)
        ref = dict((k, t) for k, t, _ in read_texts(en, tables))
        same = 0
        with open(REF_EN, "w", encoding="utf-8") as f:
            for key, text, _ in rows:
                e = ref.get(key)
                if e == text:
                    same += 1
                    continue
                f.write(json.dumps({"key": key, "ref_en": e}, ensure_ascii=False) + "\n")
        print("ref_en: %d de %d textos con inglés del PPF (%d sin traducir) -> %s"
              % (len(rows) - same, len(rows), same, REF_EN))


# ---------------------------------------------------------------- import

def load_translation():
    """Une translation/*.json (clave -> texto). Vacío si todavía no hay nada."""
    out = {}
    if not os.path.isdir(TRANSLATION):
        return out
    for dp, _dn, fn in os.walk(TRANSLATION):
        for name in sorted(fn):
            if name.endswith(".json"):
                with open(os.path.join(dp, name), encoding="utf-8") as f:
                    out.update(json.load(f))
    return out


def encode(text, key):
    try:
        return text.encode(ENC)
    except UnicodeEncodeError as e:
        raise SystemExit("%s: carácter sin código en la fuente: %r" % (key, text[e.start:e.end]))


def pack_strings(buf, o, name, texts):
    """Cadenas de una tabla empaquetadas desde el final de los registros.
    Devuelve (registros nuevos como bytes, cadenas como bytes)."""
    cnt, rs, recs = parse_table(buf, o)
    keys = table_keys(name, rs, recs)
    start = 16 + cnt * rs
    head = bytearray(buf[o:o + start])
    blob = bytearray()
    for k, r, f in keys:
        s = encode(texts[k], k) if k in texts else cstr(buf, o + recs[r][f])
        struct.pack_into("<I", head, 16 + r * rs + 4 * f, start + len(blob))
        blob += s + b"\0"
    return bytes(head), bytes(blob)


def rebuild_map_table(buf, o, name, texts):
    """Tabla de un mapa: se reescribe en su lugar, dentro del largo de datos del
    MSGa. Lo que queda después de la última cadena conserva los bytes de antes
    (restos sin apuntar, como en el original), así que el mismo texto da los
    mismos bytes. Devuelve los bytes libres que quedan."""
    head, blob = pack_strings(buf, o, name, texts)
    cap = struct.unpack_from("<I", buf, o - 0x20 + 20)[0]  # largo de datos del MSGa
    if len(head) + len(blob) > cap:
        raise SystemExit("%s: el texto no entra (%d bytes de %d)" % (name, len(head) + len(blob), cap))
    buf[o:o + len(head)] = head
    buf[o + len(head):o + len(head) + len(blob)] = blob
    return cap - len(head) - len(blob)


def build_stz(texts):
    """STAZ.STZ con los textos dados. Las tablas sueltas pueden crecer (se
    reconstruye el contenedor); las de los mapas se reescriben en su lugar."""
    data = open(STZ, "rb").read()
    c = Stz(data)
    buf = bytearray(data)
    bodies, free = {}, {}
    for name, o, kind in find_tables(data):
        if kind == "suelta":
            i = next(i for i, n in LOOSE.items() if n == name)
            head, blob = pack_strings(data, o, name, texts)
            bodies[i] = head + blob
            free[name] = len(c.body(i)) - len(bodies[i])
        else:
            free[name] = rebuild_map_table(buf, o, name, texts)
    for i, r in enumerate(c.recs):  # los mapas cambian en su lugar, sin cambiar de tamaño
        if r[6] * SECTOR < len(buf) and i not in bodies and bytes(buf[r[6] * SECTOR:r[6] * SECTOR + r[1]]) != c.body(i):
            bodies[i] = bytes(buf[r[6] * SECTOR:r[6] * SECTOR + r[1]])
    return c.build(bodies), free


def import_(out=OUT, texts=None):
    if texts is None:
        texts = load_translation()
    new, free = build_stz(texts)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "wb") as f:
        f.write(new)
    grow = {k: -v for k, v in free.items() if k.startswith("sys/") and v < 0}
    print("import: %d textos -> %s" % (len(texts), out))
    if grow:
        print("  tablas que crecen (bytes):", grow)
    return out, free


def roundtrip():
    """Ida y vuelta: exporta y vuelve a escribir todos los textos sin cambios
    (cada tabla se reempaqueta de verdad). Tiene que dar el mismo archivo."""
    export()
    texts = {}
    with open(SOURCE, encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            texts[d["key"]] = d["en"]
    out, _free = import_(os.path.join(LOCAL, "build", "roundtrip.STZ"), texts)
    ok = open(out, "rb").read() == open(STZ, "rb").read()
    print("ida y vuelta:", "IDÉNTICA" if ok else "DISTINTA")
    return ok


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "export":
        export()
    elif cmd == "import":
        import_()
    elif cmd == "roundtrip":
        sys.exit(0 if roundtrip() else 1)
    else:
        print(__doc__)
        sys.exit(2)
