#!/usr/bin/env python3
"""Mete un STAZ.STZ nuevo en una copia de la ISO japonesa de Shadow Tower Abyss.

En la ISO, `PROLOGUE.PSS` empieza justo donde termina `STAZ.STZ`, y justo antes
está `DUMMY01.OUT` (512 MB de relleno). Si el contenedor nuevo ocupa k sectores
más, `STAZ.STZ` empieza k sectores antes y `DUMMY01.OUT` pierde esos k sectores.
El juego abre el archivo por nombre (`\\TARGET\\STAZ.STZ`), no por sector.

Se actualizan los dos sistemas de archivos de la imagen: ISO9660 (registros de
directorio) y UDF (File Entry, con su CRC).

    python3 tools/ps2iso.py ISO_ORIGINAL STAZ_NUEVO ISO_SALIDA [EJECUTABLE_NUEVO]

El ejecutable (`SLPS_252.17`, con los rótulos de exe_text.py) tiene el mismo
tamaño: se escribe en su lugar.
"""
import os
import shutil
import struct
import sys

S = 2048


def both32(v):
    return struct.pack("<I", v) + struct.pack(">I", v)


def iso_records(f):
    """{ruta: (posición del registro en la imagen, LBA, tamaño)} de ISO9660."""
    f.seek(16 * S)
    pvd = f.read(S)
    assert pvd[1:6] == b"CD001"
    out = {}

    def walk(lba, size, path):
        f.seek(lba * S)
        data = f.read(size)
        o = 0
        while o < len(data):
            n = data[o]
            if n == 0:
                o = (o // S + 1) * S
                continue
            el, sz = struct.unpack_from("<I", data, o + 2)[0], struct.unpack_from("<I", data, o + 10)[0]
            flags, nl = data[o + 25], data[o + 32]
            name = data[o + 33:o + 33 + nl]
            if name not in (b"\0", b"\1"):
                p = path + "/" + name.decode().split(";")[0]
                if flags & 2:
                    walk(el, sz, p)
                else:
                    out[p] = (lba * S + o, el, sz)
            o += n

    root = pvd[156:190]
    walk(struct.unpack_from("<I", root, 2)[0], struct.unpack_from("<I", root, 10)[0], "")
    return out


def crc_itu(data):
    crc = 0
    for b in data:
        crc ^= b << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
    return crc


def udf_partition_start(f):
    for s in range(32, 256):
        f.seek(s * S)
        b = f.read(S)
        if struct.unpack_from("<H", b, 0)[0] == 5 and struct.unpack_from("<I", b, 12)[0] == s:
            return struct.unpack_from("<I", b, 188)[0]
    raise SystemExit("ISO sin partición UDF")


def udf_file_entries(f, pstart, first_file_lba):
    """{(posición relativa, tamaño): sector absoluto del File Entry}."""
    out = {}
    for s in range(pstart, first_file_lba):
        f.seek(s * S)
        b = f.read(S)
        if struct.unpack_from("<H", b, 0)[0] != 261:
            continue
        l_ea, l_ad = struct.unpack_from("<II", b, 168)
        if l_ad != 8:
            continue
        ln, pos = struct.unpack_from("<II", b, 176 + l_ea)
        out[(pos, ln)] = s
    return out


def patch_udf_fe(f, s, new_pos, new_len):
    f.seek(s * S)
    b = bytearray(f.read(S))
    l_ea = struct.unpack_from("<I", b, 168)[0]
    struct.pack_into("<Q", b, 56, new_len)                       # Information Length
    struct.pack_into("<Q", b, 64, (new_len + S - 1) // S)        # Logical Blocks Recorded
    struct.pack_into("<II", b, 176 + l_ea, new_len, new_pos)     # short_ad
    crc_len = struct.unpack_from("<H", b, 10)[0]
    struct.pack_into("<H", b, 8, crc_itu(b[16:16 + crc_len]))
    b[4] = sum(b[i] for i in range(16) if i != 4) & 0xFF
    f.seek(s * S)
    f.write(b)


def patch_iso_rec(f, pos, lba, size):
    f.seek(pos + 2)
    f.write(both32(lba))
    f.seek(pos + 10)
    f.write(both32(size))


def build(iso_in, stz_path, iso_out, exe_path=None):
    """Con `exe_path`, también escribe el ejecutable (mismo tamaño, en su lugar)."""
    new = open(stz_path, "rb").read()
    if os.path.abspath(iso_in) != os.path.abspath(iso_out):
        shutil.copyfile(iso_in, iso_out)
    with open(iso_out, "r+b") as f:
        recs = iso_records(f)
        spos, slba, ssize = recs["/TARGET/STAZ.STZ"]
        dpos, dlba, dsize = recs["/DUMMY01.OUT"]
        assert dlba * S + dsize == slba * S, "DUMMY01.OUT no está justo antes de STAZ.STZ"
        old_secs = (ssize + S - 1) // S
        new_secs = (len(new) + S - 1) // S
        k = max(0, new_secs - old_secs)
        if k * S >= dsize:
            raise SystemExit("no hay relleno suficiente en DUMMY01.OUT")
        nlba, ndsize = slba - k, dsize - k * S
        # UDF
        pstart = udf_partition_start(f)
        fes = udf_file_entries(f, pstart, min(r[1] for r in recs.values()))
        fe_s = fes[(slba - pstart, ssize)]
        fe_d = fes[(dlba - pstart, dsize)]
        # datos: el contenedor nuevo, y ceros donde sobraba el viejo
        f.seek(nlba * S)
        f.write(new)
        pad = (nlba + max(new_secs, old_secs + k)) * S - (nlba * S + len(new))
        f.write(b"\0" * pad)
        patch_iso_rec(f, spos, nlba, len(new))
        patch_udf_fe(f, fe_s, nlba - pstart, len(new))
        if k:
            patch_iso_rec(f, dpos, dlba, ndsize)
            patch_udf_fe(f, fe_d, dlba - pstart, ndsize)
        if exe_path:
            exe = open(exe_path, "rb").read()
            _epos, elba, esize = recs["/SLPS_252.17"]
            assert len(exe) == esize, "el ejecutable cambió de tamaño"
            f.seek(elba * S)
            f.write(exe)
    print("ISO: STAZ.STZ en el sector %d (%+d), %d bytes -> %s" % (nlba, -k, len(new), iso_out))


if __name__ == "__main__":
    if len(sys.argv) not in (4, 5):
        print(__doc__)
        sys.exit(2)
    build(*sys.argv[1:])
