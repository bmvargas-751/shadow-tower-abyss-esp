"""Arma el paquete de una versión: parche .xdelta, instalador .exe y LEEME.txt.

Uso:
  python3 -I tools/release.py VERSIÓN ISO_ORIGINAL [--sin-exe] [--sin-prueba-exe]

1. Arma la ISO traducida: sta_text.import_ escribe STAZ.STZ con translation/ y la
   fuente con las letras españolas y las texturas con texto (sta_tex.py), y el
   ejecutable con sus rótulos y cambios de código (exe_text.py); pss_sub.py arma
   los videos con subtítulos; ps2iso.build los mete en una copia de la ISO
   (en ../local/shadow-tower-abyss/dist/; al final se borra: solo queda el
   paquete).
2. Crea el parche con xdelta3 (`-S none` para que el instalador lo lea, y una
   ventana de 2 GB para que STAZ.STZ, que se corre unos sectores, salga como
   copia) y lo comprueba aplicándolo con xdelta3.
3. Llena tools/release/patcher.cs y LEEME.txt con la versión y las sumas, y
   compila el instalador con el csc.exe de .NET Framework 4 (Windows, desde WSL;
   la variable CSC cambia la ruta). Lo prueba con la ISO original: la ISO que
   escribe tiene que ser idéntica.
4. Empaqueta shadow-tower-abyss-esp-VERSIÓN.zip (instalador, parche y LEEME.txt)
   en ../local/shadow-tower-abyss/dist/.

Copiado de tools/release.py de Eternal Ring; cambia solo cómo se arma la ISO.
Necesita xdelta3 (la variable XDELTA3 cambia la ruta).
"""
import hashlib, os, re, shutil, subprocess, sys, zipfile, zlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import ps2iso
import pss_sub
import sta_text

LOCAL = os.path.normpath(os.path.join(ROOT, '..', 'local', 'shadow-tower-abyss'))
DIST = os.path.join(LOCAL, 'dist')
REL = os.path.join(ROOT, 'tools', 'release')
XDELTA3 = os.environ.get('XDELTA3') or shutil.which('xdelta3') or 'xdelta3'
CSC = os.environ.get('CSC', '/mnt/c/Windows/Microsoft.NET/Framework64/v4.0.30319/csc.exe')
# La ISO que espera el parche (japonesa, SLPS-25217; TECH.md).
ORIG_SIZE, ORIG_MD5 = 1561624576, 'ff48f72f5e0b4b1206469abaa24a8bd5'


def sums(path=None, stream=None):
    f = stream or open(path, 'rb')
    md5, sha1, crc, size = hashlib.md5(), hashlib.sha1(), 0, 0
    while True:
        b = f.read(1 << 24)
        if not b:
            break
        md5.update(b); sha1.update(b); crc = zlib.crc32(b, crc); size += len(b)
    return {'size': size, 'crc32': '%08x' % crc, 'md5': md5.hexdigest(), 'sha1': sha1.hexdigest()}


def winpath(p):
    return subprocess.check_output(['wslpath', '-w', p], text=True).strip()


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if len(args) != 2:
        sys.exit(__doc__)
    version, orig = args
    os.makedirs(DIST, exist_ok=True)
    name = 'shadow-tower-abyss-esp-%s' % version
    iso = os.path.join(DIST, name + '.iso')
    stz = os.path.join(DIST, 'STAZ.STZ')
    exe_new = os.path.join(DIST, 'SLPS_252.17')
    patch = os.path.join(DIST, name + '.xdelta')
    exe_name = 'Instalar Shadow Tower Abyss en español.exe'

    print('Comprobando la ISO original...')
    o = sums(orig)
    if (o['size'], o['md5']) != (ORIG_SIZE, ORIG_MD5):
        sys.exit('No es la ISO esperada: %s' % o)
    try:
        print('Armando la ISO traducida...')
        sta_text.import_(stz, exe_out=exe_new)
        videos = {pss_sub.ISO_PATHS[v]: pss_sub.build(orig, v, os.path.join(DIST, v + '.PSS'))
                  for v in pss_sub.VIDEOS}
        ps2iso.build(orig, stz, iso, exe_new, videos)
        n = sums(iso)
        print('Creando el parche...')
        subprocess.check_call([XDELTA3, '-e', '-9', '-S', 'none', '-B', str(1 << 31), '-f', '-s', orig, iso, patch])
        print('Comprobando el parche con xdelta3...')
        p = subprocess.Popen([XDELTA3, '-d', '-c', '-s', orig, patch], stdout=subprocess.PIPE)
        check = sums(stream=p.stdout)
        if p.wait() != 0 or check != n:
            sys.exit('El parche no reproduce la ISO traducida.')

        fill = {'VERSION': version, 'PATCH': os.path.basename(patch), 'EXE': exe_name,
                'ORIG_SIZE': '{:,}'.format(o['size']).replace(',', '.'), 'NEW_SIZE': '{:,}'.format(n['size']).replace(',', '.')}
        for k in ('crc32', 'md5', 'sha1'):
            fill['ORIG_' + k.upper()] = o[k]
            fill['NEW_' + k.upper()] = n[k]
        readme = open(os.path.join(REL, 'LEEME.txt'), encoding='utf-8').read()
        for k, v in fill.items():
            readme = readme.replace('{%s}' % k, v)
        assert '{' not in readme, 'LEEME.txt: falta llenar algo'
        leeme = os.path.join(DIST, 'LEEME.txt')
        with open(leeme, 'w', encoding='utf-8-sig', newline='\r\n') as w:
            w.write(readme)

        files = [(patch, os.path.basename(patch)), (leeme, 'LEEME.txt')]
        if '--sin-exe' not in sys.argv:
            src = open(os.path.join(REL, 'patcher.cs'), encoding='utf-8').read()
            for k, v in (('VERSION', version), ('SRC_SIZE', str(o['size'])), ('SRC_MD5', o['md5']),
                         ('DST_SIZE', str(n['size'])), ('DST_MD5', n['md5'])):
                src = src.replace('@%s@' % k, v)
            assert not re.search(r'@[A-Z_]+@', src), 'patcher.cs: falta llenar algo'
            cs = os.path.join(DIST, 'patcher.cs')
            with open(cs, 'w', encoding='utf-8-sig') as w:
                w.write(src)
            exe = os.path.join(DIST, 'instalador.exe')
            print('Compilando el instalador...')
            subprocess.check_call([CSC, '-nologo', '-optimize+', '-target:exe', '-codepage:65001',
                                   '-out:' + winpath(exe), '-resource:%s,patch.xdelta' % winpath(patch), winpath(cs)])
            os.chmod(exe, 0o755)
            if '--sin-prueba-exe' not in sys.argv:
                print('Probando el instalador...')
                out = os.path.join(DIST, 'prueba-exe.iso')
                try:
                    subprocess.check_call([exe, winpath(orig), winpath(out)])
                    if sums(out) != n:
                        sys.exit('El instalador no reproduce la ISO traducida.')
                finally:
                    if os.path.exists(out):
                        os.remove(out)
            files.insert(0, (exe, exe_name))
            os.remove(cs)

        pack = os.path.join(DIST, name + '.zip')
        with zipfile.ZipFile(pack, 'w', zipfile.ZIP_DEFLATED) as z:
            for path, arc in files:
                z.write(path, arc)
        print()
        print('Paquete:', pack, '(%d KB)' % (os.path.getsize(pack) // 1024))
        print('Original:  ', o)
        print('Traducida: ', n)
    finally:
        for f in [iso, stz, exe_new] + [os.path.join(DIST, v + '.PSS') for v in pss_sub.VIDEOS]:
            if os.path.exists(f):
                os.remove(f)


if __name__ == '__main__':
    main()
