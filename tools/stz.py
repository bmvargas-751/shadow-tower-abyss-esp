#!/usr/bin/env python3
"""Contenedor STAZ.STZ de Shadow Tower Abyss: lectura y reconstrucción.

Formato (TECH.md):
- Cabecera de 16 bytes: `STAZ`, tamaño total redondeado a sectores, número de
  entradas, 0x800 (tamaño de sector).
- Tabla de entradas de 32 bytes: `STZ0`, tamaño, tamaño (igual), tamaño con
  cabecera (tamaño + 32 o 48, sin regla clara: se conserva la diferencia),
  8 bytes de suma (el juego no la comprueba; el PPF inglés no la toca), sector
  de inicio y un valor fijo.
- Cada entrada empieza en su propio sector, justo después de la anterior;
  el relleno es cero y el archivo termina sin redondear.
"""
import struct

SECTOR = 0x800


def up(x):
    return (x + SECTOR - 1) // SECTOR


class Stz:
    def __init__(self, data):
        self.data = data
        assert data[:4] == b"STAZ"
        self.n = struct.unpack_from("<I", data, 8)[0]
        self.recs = [list(struct.unpack_from("<4sIIIIIII", data, 16 + i * 32)) for i in range(self.n)]
        self.first = self.recs[0][6]

    def body(self, i):
        r = self.recs[i]
        return self.data[r[6] * SECTOR:r[6] * SECTOR + r[1]]

    def build(self, bodies):
        """Arma un STAZ.STZ nuevo. `bodies` = {entrada: bytes nuevos}."""
        recs = [list(r) for r in self.recs]
        parts = []
        sec = self.first
        for i, r in enumerate(recs):
            b = bodies.get(i)
            if b is None:
                b = self.body(i)
            extra = r[3] - r[1]
            r[1] = r[2] = len(b)
            r[3] = len(b) + extra
            r[6] = sec
            parts.append(b)
            sec += up(len(b))
        head = bytearray(self.data[:self.first * SECTOR])
        for i, r in enumerate(recs):
            struct.pack_into("<4sIIIIIII", head, 16 + i * 32, *r)
        total = recs[-1][6] * SECTOR + recs[-1][1]
        struct.pack_into("<I", head, 4, up(total) * SECTOR)
        out = bytearray(head)
        for i, b in enumerate(parts):
            out += b
            if i + 1 < len(parts):
                out += b"\0" * (up(len(b)) * SECTOR - len(b))
        assert len(out) == total
        return bytes(out)


if __name__ == "__main__":
    import sys
    data = open(sys.argv[1], "rb").read()
    same = Stz(data).build({}) == data
    print("reconstrucción sin cambios:", "IDÉNTICA" if same else "DISTINTA")
    sys.exit(0 if same else 1)
