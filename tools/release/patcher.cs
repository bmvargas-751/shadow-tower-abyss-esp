// Instalador de Shadow Tower Abyss en español para Windows.
//
// Lleva adentro el parche .xdelta (VCDIFF, RFC 3284) y lo aplica a la ISO japonesa
// del usuario: comprueba la copia, escribe «Shadow Tower Abyss (Español).iso» al lado
// (la original no se toca) y comprueba el resultado. tools/release.py llena los
// valores @...@ y lo compila con el csc.exe de .NET Framework 4 (C# 5).
//
// Uso: arrastrar la ISO a la ventana, o
//      instalador.exe ISO_ORIGINAL [ISO_NUEVA]   (con dos argumentos no hace pausas)
using System;
using System.IO;
using System.Reflection;
using System.Security.Cryptography;
using System.Text;

static class Instalador
{
    const string Version = "@VERSION@";
    const long SrcSize = @SRC_SIZE@;
    const string SrcMd5 = "@SRC_MD5@";
    const long DstSize = @DST_SIZE@;
    const string DstMd5 = "@DST_MD5@";
    const string OutName = "Shadow Tower Abyss (Español).iso";

    static bool pause = true;

    static int Main(string[] args)
    {
        try { Console.OutputEncoding = Encoding.UTF8; } catch (Exception) { }
        Console.Title = "Shadow Tower Abyss en español " + Version;
        try
        {
            return Run(args);
        }
        catch (Exception e)
        {
            Console.WriteLine();
            Console.WriteLine("No se pudo terminar: " + e.Message);
            Pause();
            return 1;
        }
    }

    static int Run(string[] args)
    {
        Console.WriteLine("Shadow Tower Abyss en español, versión " + Version);
        Console.WriteLine("Traducción fan. No incluye el juego: se aplica a tu propia copia.");
        Console.WriteLine();
        string src;
        string dst = null;
        if (args.Length >= 1)
            src = args[0];
        else
        {
            Console.WriteLine("Arrastra a esta ventana tu ISO de Shadow Tower Abyss (japonesa, SLPS-25217)");
            Console.Write("y presiona Enter: ");
            src = Console.ReadLine() ?? "";
        }
        if (args.Length >= 2) { dst = args[1]; pause = false; }
        src = src.Trim().Trim('"').Trim();
        if (src.Length == 0 || !File.Exists(src))
            return Fail("No encuentro ese archivo: " + src);
        src = Path.GetFullPath(src);
        if (dst == null)
            dst = Path.Combine(Path.GetDirectoryName(src), OutName);
        dst = Path.GetFullPath(dst);

        long size = new FileInfo(src).Length;
        if (size != SrcSize)
            return Fail("Esta ISO no es la que espera el parche: mide " + size.ToString("N0") + " bytes y la japonesa " +
                        "(SLPS-25217) mide " + SrcSize.ToString("N0") + ". Si tu copia está en otro formato (.chd, .cso, .bin), " +
                        "pásala primero a .iso.");

        Console.WriteLine();
        string md5 = Md5(src, "Comprobando tu copia");
        if (md5 == DstMd5)
            return Fail("Esta ISO ya está traducida.");
        if (md5 != SrcMd5)
            return Fail("Esta ISO no es la que espera el parche (MD5 " + md5 + ", se espera " + SrcMd5 + "). " +
                        "Hace falta la versión japonesa (SLPS-25217), sin modificar.");

        if (string.Equals(src, dst, StringComparison.OrdinalIgnoreCase))
            return Fail("La ISO nueva no puede reemplazar a la original.");
        if (File.Exists(dst) && pause)
        {
            Console.Write("Ya existe «" + Path.GetFileName(dst) + "». ¿La reemplazo? (s/n): ");
            string a = (Console.ReadLine() ?? "").Trim().ToLowerInvariant();
            if (a != "s" && a != "si" && a != "sí")
                return Fail("No se tocó nada.");
        }
        try
        {
            DriveInfo d = new DriveInfo(Path.GetPathRoot(dst));
            long have = d.AvailableFreeSpace + (File.Exists(dst) ? new FileInfo(dst).Length : 0);
            if (have < DstSize)
                return Fail("No hay espacio: la ISO traducida necesita " + (DstSize >> 20).ToString("N0") + " MB libres en " + d.Name + ".");
        }
        catch (ArgumentException) { }   // rutas de red: sin comprobación

        string tmp = dst + ".part";
        try
        {
            using (Stream patch = Assembly.GetExecutingAssembly().GetManifestResourceStream("patch.xdelta"))
            using (FileStream s = new FileStream(src, FileMode.Open, FileAccess.Read, FileShare.Read, 1 << 20))
            using (FileStream o = new FileStream(tmp, FileMode.Create, FileAccess.Write, FileShare.None, 1 << 20))
            {
                Vcdiff.Apply(new BufferedStream(patch), s, o, delegate(long done)
                {
                    Progress("Aplicando la traducción", done, DstSize);
                });
            }
            Console.WriteLine();
            if (new FileInfo(tmp).Length != DstSize)
                throw new InvalidDataException("la ISO traducida no tiene el tamaño esperado.");
            if (Md5(tmp, "Comprobando la ISO traducida") != DstMd5)
                throw new InvalidDataException("la ISO traducida no salió como debía. Vuelve a intentarlo.");
            if (File.Exists(dst)) File.Delete(dst);
            File.Move(tmp, dst);
        }
        catch (Exception)
        {
            try { if (File.Exists(tmp)) File.Delete(tmp); } catch (Exception) { }
            throw;
        }

        Console.WriteLine();
        Console.WriteLine("Listo. La traducción quedó en:");
        Console.WriteLine("  " + dst);
        Console.WriteLine("Ábrela en PCSX2. Tu ISO original no se tocó.");
        Pause();
        return 0;
    }

    static int Fail(string msg)
    {
        Console.WriteLine();
        Console.WriteLine(msg);
        Pause();
        return 1;
    }

    static void Pause()
    {
        if (!pause) return;
        Console.WriteLine();
        Console.Write("Presiona Enter para cerrar.");
        Console.ReadLine();
    }

    static int lastPct = -1;

    static void Progress(string what, long done, long total)
    {
        int pct = (int)(done * 100 / Math.Max(total, 1));
        if (pct == lastPct) return;
        lastPct = pct;
        Console.Write("\r" + what + "... " + pct + " %   ");
    }

    static string Md5(string path, string what)
    {
        lastPct = -1;
        using (MD5 h = MD5.Create())
        using (FileStream f = new FileStream(path, FileMode.Open, FileAccess.Read, FileShare.Read, 1 << 20))
        {
            byte[] buf = new byte[4 << 20];
            long total = f.Length, done = 0;
            int n;
            while ((n = f.Read(buf, 0, buf.Length)) > 0)
            {
                h.TransformBlock(buf, 0, n, null, 0);
                done += n;
                Progress(what, done, total);
            }
            h.TransformFinalBlock(buf, 0, 0);
            Console.WriteLine();
            StringBuilder sb = new StringBuilder();
            foreach (byte b in h.Hash) sb.Append(b.ToString("x2"));
            return sb.ToString();
        }
    }
}

// Decodificador VCDIFF (RFC 3284) con lo que usa xdelta3 -S none: tabla de
// códigos por defecto, ventanas con VCD_SOURCE y suma Adler-32 por ventana.
static class Vcdiff
{
    const int NOOP = 0, ADD = 1, RUN = 2, COPY = 3;
    const int NEAR = 4, SAME = 3;
    static readonly byte[] T1 = new byte[256], S1 = new byte[256], M1 = new byte[256];
    static readonly byte[] T2 = new byte[256], S2 = new byte[256], M2 = new byte[256];

    static Vcdiff()
    {
        int i = 0;
        T1[i] = RUN; S1[i] = 0; i++;
        for (int s = 0; s <= 17; s++) { T1[i] = ADD; S1[i] = (byte)s; i++; }
        for (int m = 0; m < 9; m++)
        {
            T1[i] = COPY; S1[i] = 0; M1[i] = (byte)m; i++;
            for (int s = 4; s <= 18; s++) { T1[i] = COPY; S1[i] = (byte)s; M1[i] = (byte)m; i++; }
        }
        for (int m = 0; m < 6; m++)
            for (int a = 1; a <= 4; a++)
                for (int c = 4; c <= 6; c++)
                { T1[i] = ADD; S1[i] = (byte)a; T2[i] = COPY; S2[i] = (byte)c; M2[i] = (byte)m; i++; }
        for (int m = 6; m < 9; m++)
            for (int a = 1; a <= 4; a++)
            { T1[i] = ADD; S1[i] = (byte)a; T2[i] = COPY; S2[i] = 4; M2[i] = (byte)m; i++; }
        for (int m = 0; m < 9; m++)
        { T1[i] = COPY; S1[i] = 4; M1[i] = (byte)m; T2[i] = ADD; S2[i] = 1; i++; }
        if (i != 256) throw new InvalidOperationException("tabla de códigos");
    }

    static int Byte(Stream p)
    {
        int b = p.ReadByte();
        if (b < 0) throw new InvalidDataException("el parche está incompleto.");
        return b;
    }

    static long Int(Stream p)
    {
        long v = 0;
        for (int k = 0; k < 10; k++)
        {
            int b = Byte(p);
            v = (v << 7) + (b & 0x7f);
            if ((b & 0x80) == 0) return v;
        }
        throw new InvalidDataException("el parche está dañado.");
    }

    static long Int(byte[] a, ref int i)
    {
        long v = 0;
        for (int k = 0; k < 10; k++)
        {
            if (i >= a.Length) throw new InvalidDataException("el parche está dañado.");
            int b = a[i++];
            v = (v << 7) + (b & 0x7f);
            if ((b & 0x80) == 0) return v;
        }
        throw new InvalidDataException("el parche está dañado.");
    }

    static byte[] Bytes(Stream p, long n)
    {
        byte[] a = new byte[checked((int)n)];
        int got = 0;
        while (got < a.Length)
        {
            int r = p.Read(a, got, a.Length - got);
            if (r <= 0) throw new InvalidDataException("el parche está incompleto.");
            got += r;
        }
        return a;
    }

    static void ReadAt(FileStream f, long pos, byte[] dst, int off, int n)
    {
        f.Seek(pos, SeekOrigin.Begin);
        while (n > 0)
        {
            int r = f.Read(dst, off, n);
            if (r <= 0) throw new InvalidDataException("tu ISO es más corta de lo esperado.");
            off += r; n -= r;
        }
    }

    static uint Adler32(byte[] a, int n)
    {
        uint s1 = 1, s2 = 0;
        int i = 0;
        while (i < n)
        {
            int end = Math.Min(n, i + 5552);
            for (; i < end; i++) { s1 += a[i]; s2 += s1; }
            s1 %= 65521; s2 %= 65521;
        }
        return (s2 << 16) | s1;
    }

    public static void Apply(Stream p, FileStream src, Stream dst, Action<long> progress)
    {
        if (Byte(p) != 0xD6 || Byte(p) != 0xC3 || Byte(p) != 0xC4)
            throw new InvalidDataException("el parche no es un archivo VCDIFF.");
        Byte(p);                                              // versión
        int hdr = Byte(p);
        if ((hdr & 0x01) != 0) throw new InvalidDataException("el parche usa compresión secundaria.");
        if ((hdr & 0x02) != 0) throw new InvalidDataException("el parche usa una tabla de códigos propia.");
        if ((hdr & 0x04) != 0) Bytes(p, Int(p));              // datos de la aplicación (xdelta3)
        long written = 0;
        long[] near = new long[NEAR];
        long[] same = new long[SAME * 256];
        while (true)
        {
            int win = p.ReadByte();
            if (win < 0) break;
            if ((win & 0x02) != 0) throw new InvalidDataException("el parche copia de la salida (VCD_TARGET).");
            long srcLen = 0, srcPos = 0;
            if ((win & 0x01) != 0) { srcLen = Int(p); srcPos = Int(p); }
            Int(p);                                           // largo de la codificación
            int tLen = checked((int)Int(p));
            if (Byte(p) != 0) throw new InvalidDataException("el parche usa compresión secundaria.");
            long dataLen = Int(p), instLen = Int(p), addrLen = Int(p);
            bool hasSum = (win & 0x04) != 0;
            uint sum = 0;
            if (hasSum) for (int k = 0; k < 4; k++) sum = (sum << 8) | (uint)Byte(p);
            byte[] data = Bytes(p, dataLen), inst = Bytes(p, instLen), addr = Bytes(p, addrLen);

            byte[] t = new byte[tLen];
            int tp = 0, di = 0, ii = 0, ai = 0, nextSlot = 0;
            Array.Clear(near, 0, near.Length);
            Array.Clear(same, 0, same.Length);
            while (ii < inst.Length)
            {
                int code = inst[ii++];
                for (int half = 0; half < 2; half++)
                {
                    int type = half == 0 ? T1[code] : T2[code];
                    if (type == NOOP) continue;
                    long size = half == 0 ? S1[code] : S2[code];
                    int mode = half == 0 ? M1[code] : M2[code];
                    if (size == 0) size = Int(inst, ref ii);
                    int n = checked((int)size);
                    if (tp + n > tLen) throw new InvalidDataException("el parche está dañado (ventana).");
                    if (type == ADD)
                    {
                        Buffer.BlockCopy(data, di, t, tp, n);
                        di += n; tp += n;
                    }
                    else if (type == RUN)
                    {
                        byte b = data[di++];
                        for (int k = 0; k < n; k++) t[tp++] = b;
                    }
                    else
                    {
                        long here = srcLen + tp, a;
                        if (mode == 0) a = Int(addr, ref ai);
                        else if (mode == 1) a = here - Int(addr, ref ai);
                        else if (mode < 2 + NEAR) a = near[mode - 2] + Int(addr, ref ai);
                        else a = same[(mode - 2 - NEAR) * 256 + addr[ai++]];
                        near[nextSlot] = a; nextSlot = (nextSlot + 1) % NEAR;
                        same[a % (SAME * 256)] = a;
                        if (a < 0 || a >= here) throw new InvalidDataException("el parche está dañado (dirección).");
                        if (a < srcLen)
                        {
                            int m = (int)Math.Min(n, srcLen - a);
                            ReadAt(src, srcPos + a, t, tp, m);
                            tp += m; n -= m; a += m;
                        }
                        for (long ta = a - srcLen; n > 0; n--) t[tp++] = t[ta++];   // byte a byte: puede solaparse
                    }
                }
            }
            if (tp != tLen) throw new InvalidDataException("el parche está dañado (largo).");
            if (hasSum && Adler32(t, tLen) != sum) throw new InvalidDataException("tu ISO no coincide con la del parche.");
            dst.Write(t, 0, tLen);
            written += tLen;
            progress(written);
        }
    }
}
