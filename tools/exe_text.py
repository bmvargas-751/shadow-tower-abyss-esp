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

# Rótulos que ve el jugador, por pantalla (dirección virtual). En «equipo», los
# estados alterados (tabla de punteros en 0x1f2690) se van mostrando de a uno. Quedan fuera las
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
    "equipo": [0x1fcb08, 0x1fcb18, 0x1fc980, 0x1fc988, 0x1fc998, 0x1fc9a8, 0x1fc9b0, 0x1fc9b8],
    "pausa": [0x1fd610, 0x1fd618, 0x1fd628, 0x1fd638, 0x1fd648, 0x1fd650, 0x1fd660],
    "tienda": [0x1fd830, 0x1fd840, 0x1fd850, 0x1fd860,
               0x1fe7d0, 0x1fe7d8, 0x1fe7e0, 0x1fe7e8, 0x1fe7f0, 0x1fe7f8],
}
SCREEN = {a: s for s, v in LABELS.items() for a in v}


# Estrechar a lo ancho (TECH.md, «Ejecutable»). El dibujador de texto (0x188010)
# lee dos escalas de su registro: +0x20, la del texto entero, y +0x24, que solo
# multiplica el ancho de cada letra y su avance. Las funciones que lo llaman dejan
# +0x24 en 1.0. El cambio hace que 0x1874f0 (dibujo con espaciado, alineación y
# escala) tome +0x24 de los bits altos de su tercer argumento: a2 = alineación
# (bits 0-2) | bits de un float con los 3 últimos en 0. Las otras dos llamadas
# (0x1917f0, 0x1dd18c) pasan a2 = 0, así que quedan con 1.0, como antes.
DRAW_AT = 0x1874f0
DRAW_ORIG = [
    0x27bdff70, 0xffbf0040, 0x7fb20030, 0x7fb10020, 0x0080902d, 0x7fb00010, 0x00a0882d, 0xe7b60008,
    0x00c0802d, 0xe7b50004, 0xe7b40000, 0xafa7005c, 0x46006586, 0x46006d46, 0x12200019, 0x46007506,
    0x0c049780, 0x0220202d, 0x0002303c, 0x0220282d, 0x0006303e, 0x0c061ea4, 0x27a40060, 0x3c023f80,
    0x8fa5005c, 0xafa20084, 0x2403fff8, 0x3c024580, 0x32060007, 0xafa20074, 0x27a40060, 0x93a20068,
    0xe7b60060, 0xe7b50064, 0xa7b2006c, 0xe7b40080, 0x00431024, 0x00461025, 0x0c062004, 0xa3a20068,
    0xdfbf0040, 0x7bb20030, 0xc7b60008, 0x7bb10020, 0xc7b50004, 0x7bb00010, 0xc7b40000, 0x03e00008,
    0x27bd0090, 0x00000000, 0x00000000, 0x00000000,
]
DRAW_CODE = (DRAW_ORIG[:14] + [0x1220001c] + DRAW_ORIG[15:25] + [   # beq s1,zero: el salto, 3 más allá
    0x001008c2,  # srl  at,s0,3
    0x000108c0,  # sll  at,at,3           a2 sin la alineación
    0x0021100b,  # movn v0,at,at          si hay escala a lo ancho, en vez de 1.0
] + DRAW_ORIG[25:49])                     # sw v0,132(sp) = +0x24; los 3 nop del final se usan


def hscale(f):
    """Bits altos de a2 para una escala a lo ancho `f` (lui: 16 bits)."""
    return struct.unpack(">I", struct.pack(">f", f))[0] >> 16


# Rótulos de la configuración de botones. La función 0x1907d0 los dibuja
# centrados; los de 9 bytes o más, con las letras juntas (-2 por letra; -3 en
# 移動・旋回 y -7 en 左/右平行移動), pensado para kanji: el español se encima
# («LATERALIZQ») o se sale del recuadro. El cambio reescribe el final de la
# función (0x1909a0–0x190a24) para que todos los rótulos pasen por 0x1874f0:
# espaciado 0 los cortos y -2 los largos, y si el primer renglón mide más de
# FIT_WIDTH (el recuadro mide unos 100), se estrecha solo a lo ancho lo justo
# para que entre: todos quedan de la misma altura. Para medir convierte el texto
# como el dibujador (0x1e5c60 al búfer 0x48d360) y usa su medida (0x1889e0).
FIT_AT = 0x1909a0
FIT_WIDTH = 96.0
# Los rótulos que dibuja esa función (tabla de punteros en 0x1f2bb0). Más
# estrechos que la mitad (ancho > FIT_WIDTH / FIT_MIN) ya no se leen bien: el
# chequeo de la caja avisa (hooks.py). Solo se mide el primer renglón.
FIT_LABELS = [0x1fcf98, 0x1fcfa0, 0x1fcfb0, 0x1fcfc0, 0x1fcfc8, 0x1fcfd8, 0x1fcfe8, 0x1fcff0,
              0x1fcff8, 0x1fd000, 0x1fd010, 0x1fd020, 0x1fd030, 0x1fd040, 0x1fd050, 0x1fd058,
              0x1fd068, 0x1fd078, 0x1fd088, 0x1fd090]
FIT_MIN = 0.5
FIT_ORIG = [
    0x2c410009, 0x14200018, 0x00000000, 0x24020001, 0x16420003, 0x00000000, 0x2411fffd, 0x00000000,
    0x24020004, 0x12420004, 0x24020005, 0x16420004, 0x00000000, 0x00000000, 0x2411fff9, 0x00000000,
    0x8e050000, 0xc66c0038, 0x8fa7007c, 0xc66d003c, 0x0220202d, 0x4600a386, 0x0c061d3c, 0x24060001,
    0x10000009, 0x00000000, 0x8e040000, 0xc66c0038, 0x8fa6007c, 0xc66d003c, 0x3c023f80, 0x44827000,
    0x0c061d70, 0x24050001,
]
FIT_CODE = [
    0x2c410009,  # sltiu at,v0,9          v0 = bytes del rótulo
    0x0001880b,  # movn  s1,zero,at       los cortos, sin juntar las letras (s1 = -2)
    0x0040382d,  # daddu a3,v0,zero
    0x3c040049,  # lui   a0,0x49
    0x2484d360,  # addiu a0,a0,-11424     búfer 0x48d360
    0x24050800,  # addiu a1,zero,2048
    0x0c079718,  # jal   0x1e5c60         convierte el texto (como el dibujador)
    0x8e060000,  # lw    a2,0(s0)
    0x3c040049,  # lui   a0,0x49
    0x2484d360,  # addiu a0,a0,-11424
    0x0220282d,  # daddu a1,s1,zero       espaciado
    0x3c023f80,  # lui   v0,0x3f80
    0x44826800,  # mtc1  v0,$f13          a lo ancho, 1.0
    0x0c062278,  # jal   0x1889e0         ancho del primer renglón -> $f0
    0x4600a306,  # mov.s $f12,$f20        escala (0.95 en 攻撃・銃解除, si no 1.0)
    0x3c0242c0,  # lui   v0,0x42c0        96.0 (FIT_WIDTH)
    0x44820800,  # mtc1  v0,$f1
    0x24060001,  # addiu a2,zero,1        centrado, sin estrechar
    0x46000834,  # c.lt.s $f1,$f0
    0x45000006,  # bc1f  0x190a08         si entra, sigue igual
    0x46000843,  # div.s $f1,$f1,$f0      (siempre; se usa solo si no entra)
    0x44060800,  # mfc1  a2,$f1           96 / ancho
    0x00000000,  # nop
    0x000630c2,  # srl   a2,a2,3
    0x000630c0,  # sll   a2,a2,3
    0x34c60001,  # ori   a2,a2,1          centrado y estrechado a lo ancho
    0x8e050000,  # lw    a1,0(s0)
    0xc66c0038,  # lwc1  $f12,56(s3)      x
    0x8fa7007c,  # lw    a3,124(sp)       color
    0xc66d003c,  # lwc1  $f13,60(s3)      y
    0x0220202d,  # daddu a0,s1,zero
    0x4600a386,  # mov.s $f14,$f20
    0x0c061d3c,  # jal   0x1874f0         dibuja
    0x00000000,  # nop
]

# Guardar y cargar (dos pantallas: 0x18bxxx y 0x192xxx). El tiempo y el nombre
# del lugar van al 90% y alineados a la izquierda con 0x1875c0; en español se
# salen de su franja (el lugar, también en inglés). Se dibujan con 0x1874f0,
# estrechados a lo ancho por igual: SAVE_TIME y SAVE_PLACE. La escala queda en
# 0x3f660000 (0.898) en vez de 0.9 para que entre la instrucción de más.
SAVE_TIME = 0.83       # «TIEMPO  0:13:59» (172) como «TIME  0:13:59» (144)
SAVE_PLACE = 0.75      # el lugar más ancho (215) en ~145, la franja mide unos 150


def _save(color, text, hs):
    """lwc1 x; lw a3,color(sp); lwc1 y; lui escala; texto -> a1; mtc1; lui a2; jal 0x1874f0; a0 = 0."""
    return [0xc68c0038, 0x8fa70000 | color, 0xc68d003c] + text + [0x3c060000 | hscale(hs), 0x0c061d3c, 0x0000202d]


SAVE_PATCHES = {
    0x18bf64: ([0xc68c0038, 0x8fa601bc, 0xc68d003c, 0x3c023f66, 0x34426666, 0x27a400a0, 0x44827000, 0x0c061d70, 0x0000282d],
               _save(0x1bc, [0x3c023f66, 0x27a500a0, 0x44827000], SAVE_TIME)),    # addiu a1,sp,160
    0x18bfb8: ([0xc68c0038, 0x8fa601bc, 0xc68d003c, 0x3c033f66, 0x34636666, 0x0040202d, 0x44837000, 0x0c061d70, 0x0000282d],
               _save(0x1bc, [0x3c033f66, 0x0040282d, 0x44837000], SAVE_PLACE)),   # daddu a1,v0,zero
    0x1923b4: ([0xc68c0038, 0x8fa601ac, 0xc68d003c, 0x3c023f66, 0x34426666, 0x27a40090, 0x44827000, 0x0c061d70, 0x0000282d],
               _save(0x1ac, [0x3c023f66, 0x27a50090, 0x44827000], SAVE_TIME)),    # addiu a1,sp,144
    0x192408: ([0xc68c0038, 0x8fa601ac, 0xc68d003c, 0x3c033f66, 0x34636666, 0x0040202d, 0x44837000, 0x0c061d70, 0x0000282d],
               _save(0x1ac, [0x3c033f66, 0x0040282d, 0x44837000], SAVE_PLACE)),
}

# Nombres de las listas (enciclopedia, y las demás que usan el mismo dibujo): la
# función 0x180ca0 los dibuja centrados en su barra (x + 96) con 0x1875c0, al
# 100%. En español muchos se salen de la barra. La llamada (0x180edc) pasa a una
# rutina nueva con la misma firma que 0x1875c0, escrita en el lugar de una
# función que nada usa (0x1025d0, 96 instrucciones; ni llamadas, ni punteros, ni
# saltos desde afuera): mide el texto como el dibujador y, si pasa de
# LIST_WIDTH, lo estrecha a lo ancho lo justo para que entre (0x1874f0).
LIST_AT = 0x1025d0
LIST_WIDTH = 176.0     # la barra mide unos 192 (la rutina centra en x + 96)
LIST_ORIG = [
    0x27bdffa0, 0x3c021000, 0xffb30030, 0x34423840, 0xffbf0050, 0x0080982d, 0xffb20020, 0xffb10010,
    0xffb00000, 0xffb40040, 0x0c040960, 0x8c540000, 0x2c420002, 0x14400003, 0x3c021000, 0x10000048,
    0x0000102d, 0x3c031000, 0x34423900, 0x34633910, 0x8c450000, 0x3c041000, 0x34843920, 0x3c061000,
    0xae650000, 0x34c63930, 0x3c051000, 0x3c0f1000, 0x8c620000, 0x34a53940, 0x35ef3950, 0x3c101000,
    0xae620004, 0x36103960, 0x3c0e1000, 0x3c111000, 0x8c820000, 0x35ce3970, 0x36313870, 0x3c0c1000,
    0xae620008, 0x358c3880, 0x3c0b1000, 0x3c0d1000, 0x8cc20000, 0x356b3800, 0x35ad38d0, 0x3c061000,
    0xae62000c, 0x34c63890, 0x3c071000, 0x3c091000, 0x8ca20000, 0x34e73830, 0x35293860, 0x3c081000,
    0xae620010,
]
LIST_CODE = [
    0x27bdffb0,  # addiu sp,sp,-80
    0x7fb00000,  # sq    s0,0(sp)
    0x7fb10010,  # sq    s1,16(sp)
    0x7fb20020,  # sq    s2,32(sp)
    0xffbf0030,  # sd    ra,48(sp)
    0xe7b40038,  # swc1  $f20,56(sp)
    0xe7b5003c,  # swc1  $f21,60(sp)
    0xe7b60040,  # swc1  $f22,64(sp)
    0x0080802d,  # daddu s0,a0,zero       texto
    0x00a0882d,  # daddu s1,a1,zero       alineación
    0x00c0902d,  # daddu s2,a2,zero       color
    0x46006506,  # mov.s $f20,$f12        x
    0x46006d46,  # mov.s $f21,$f13        y
    0x12000022,  # beq   s0,zero,0x102690 sin texto, nada
    0x46007586,  # mov.s $f22,$f14        escala
    0x0c049780,  # jal   0x125e00         largo -> v0
    0x0200202d,  # daddu a0,s0,zero
    0x3c040049,  # lui   a0,0x49
    0x2484d360,  # addiu a0,a0,-11424     búfer 0x48d360
    0x24050800,  # addiu a1,zero,2048
    0x0200302d,  # daddu a2,s0,zero
    0x0c079718,  # jal   0x1e5c60         convierte el texto (como el dibujador)
    0x0040382d,  # daddu a3,v0,zero
    0x3c040049,  # lui   a0,0x49
    0x2484d360,  # addiu a0,a0,-11424
    0x0000282d,  # daddu a1,zero,zero     espaciado 0
    0x3c023f80,  # lui   v0,0x3f80
    0x44826800,  # mtc1  v0,$f13          a lo ancho, 1.0
    0x0c062278,  # jal   0x1889e0         ancho -> $f0
    0x4600b306,  # mov.s $f12,$f22
    0x3c024330,  # lui   v0,0x4330        176.0 (LIST_WIDTH)
    0x44820800,  # mtc1  v0,$f1
    0x0220302d,  # daddu a2,s1,zero       alineación, sin estrechar
    0x46000834,  # c.lt.s $f1,$f0
    0x45000006,  # bc1f  0x102674         si entra, sigue igual
    0x46000843,  # div.s $f1,$f1,$f0
    0x44020800,  # mfc1  v0,$f1
    0x00000000,  # nop
    0x000210c2,  # srl   v0,v0,3
    0x000210c0,  # sll   v0,v0,3
    0x00c23025,  # or    a2,a2,v0         estrechado a lo ancho
    0x0000202d,  # daddu a0,zero,zero     espaciado 0
    0x0200282d,  # daddu a1,s0,zero
    0x0240382d,  # daddu a3,s2,zero
    0x4600a306,  # mov.s $f12,$f20
    0x4600ab46,  # mov.s $f13,$f21
    0x0c061d3c,  # jal   0x1874f0         dibuja
    0x4600b386,  # mov.s $f14,$f22
    0x7bb00000,  # lq    s0,0(sp)
    0x7bb10010,  # lq    s1,16(sp)
    0x7bb20020,  # lq    s2,32(sp)
    0xdfbf0030,  # ld    ra,48(sp)
    0xc7b40038,  # lwc1  $f20,56(sp)
    0xc7b5003c,  # lwc1  $f21,60(sp)
    0xc7b60040,  # lwc1  $f22,64(sp)
    0x03e00008,  # jr    ra
    0x27bd0050,  # addiu sp,sp,80
]
assert hscale(LIST_WIDTH) == LIST_CODE[30] & 0xffff
LIST_CALL = 0x180edc   # jal 0x1875c0 -> jal LIST_AT

# Todos los cambios de código: {dirección: (original, nuevo)}.
PATCHES = {DRAW_AT: (DRAW_ORIG, DRAW_CODE), FIT_AT: (FIT_ORIG, FIT_CODE), **SAVE_PATCHES,
           LIST_AT: (LIST_ORIG, LIST_CODE), LIST_CALL: ([0x0c061d70], [0x0c000000 | LIST_AT >> 2])}
for _o, _n in PATCHES.values():
    assert len(_o) == len(_n)
assert len(FIT_CODE) == len(FIT_ORIG)
assert struct.unpack(">I", struct.pack(">f", FIT_WIDTH))[0] >> 16 == FIT_CODE[15] & 0xffff


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


def patch_code(d):
    """Aplica en `d` (bytearray del ejecutable) los cambios de código (PATCHES)."""
    for at, (orig, code) in PATCHES.items():
        o = at - BASE
        now = list(struct.unpack_from("<%dI" % len(orig), d, o))
        if now == code:
            continue
        assert now == orig, "exe: el código en 0x%06x no es el esperado" % at
        struct.pack_into("<%dI" % len(code), d, o, *code)


def build(texts, font=True):
    """Ejecutable con los textos dados ({clave: texto}); lo que falta queda como
    el original. Con `font`, las letras españolas van con sus códigos prestados
    y se aplican los cambios de código (patch_code)."""
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
    if font:
        patch_code(d)
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
