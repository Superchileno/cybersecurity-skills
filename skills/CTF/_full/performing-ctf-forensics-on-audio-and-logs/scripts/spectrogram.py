#!/usr/bin/env python3
"""Genera espectrogramas de un audio (wrapper de sox o fallback con numpy).

Uso:
    python spectrogram.py audio.wav --out work/
    python spectrogram.py audio.wav --out work/ --start 0 --duration 5
    python spectrogram.py audio.wav --out work/ --dynamic 110 --width 1600

Salidas: spec.png (completo), spec_<canal>.png si es estéreo, y spec_zoom.png
si se indica --start/--duration.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys

try:
    import numpy as np
except ImportError:
    np = None


def con_sox(archivo: str, salida: str, inicio: float | None, duracion: float | None,
            ancho: int, alto: int, dinamico: float) -> bool:
    if not shutil.which("sox"):
        return False
    cmd = ["sox", archivo]
    if inicio is not None or duracion is not None:
        cmd += ["trim", str(inicio or 0), str(duracion)] if duracion else ["trim", str(inicio)]
        # sox: 'trim start duration' ; si falta duracion se usa '='
        if duracion is None:
            cmd = ["sox", archivo, "trim", str(inicio or 0)]
    cmd += ["-n", "spectrogram", "-o", salida, "-x", str(ancho),
            "-y", str(alto), "-z", str(int(dinamico))]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[!] sox falló: {res.stderr.strip()}")
        return False
    return True


def con_numpy(archivo: str, salida: str) -> bool:
    if np is None:
        return False
    try:
        import wave
        from PIL import Image
    except ImportError:
        return False
    try:
        with wave.open(archivo, "rb") as w:
            sr = w.getframerate()
            canales = w.getnchannels()
            sw = w.getsampwidth()
            frames = w.readframes(w.getnframes())
    except Exception as exc:  # noqa: BLE001
        print(f"[!] no se pudo leer WAV: {exc}")
        return False
    dtype = {1: np.uint8, 2: "<i2", 4: "<i4"}.get(sw)
    if dtype is None:
        return False
    data = np.frombuffer(frames, dtype=dtype)
    if canales > 1:
        data = data.reshape(-1, canales)[:, 0]

    nfft = 2048
    hop = nfft // 4
    ventana = np.hanning(nfft)
    columnas = []
    for i in range(0, len(data) - nfft, hop):
        seg = data[i:i + nfft].astype(np.float64) * ventana
        mag = np.abs(np.fft.rfft(seg))
        columnas.append(20 * np.log10(mag + 1e-9))
    if not columnas:
        return False
    spec = np.array(columnas).T
    spec -= spec.min()
    spec /= max(spec.max(), 1e-9)
    img = (spec[::-1] * 255).astype(np.uint8)
    Image.fromarray(img).save(salida)
    print(f"[i] espectrograma generado con numpy ({sr} Hz)")
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description="Espectrograma de audio")
    ap.add_argument("audio")
    ap.add_argument("--out", default="work")
    ap.add_argument("--start", type=float)
    ap.add_argument("--duration", type=float)
    ap.add_argument("--width", type=int, default=1400)
    ap.add_argument("--height", type=int, default=700)
    ap.add_argument("--dynamic", type=float, default=90.0)
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    base = os.path.splitext(os.path.basename(args.audio))[0]
    nombre = "spec_zoom.png" if args.start is not None else "spec.png"
    salida = os.path.join(args.out, nombre)

    ok = con_sox(args.audio, salida, args.start, args.duration,
                 args.width, args.height, args.dynamic)
    if not ok:
        salida = os.path.join(args.out, "spec.png")
        ok = con_numpy(args.audio, salida)
    if not ok:
        print("[!] instala sox o pillow+numpy")
        return 1

    print(f"[+] {salida}")
    print("    Si el texto es tenue: subir --dynamic, ampliar y aplicar autocontraste")
    print("    OCR: tesseract spec.png out --psm 7 -c "
          "tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")
    return 0


if __name__ == "__main__":
    sys.exit(main())
