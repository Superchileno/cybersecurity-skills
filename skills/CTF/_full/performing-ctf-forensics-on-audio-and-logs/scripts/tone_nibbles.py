#!/usr/bin/env python3
"""Decodifica tonos duales (nibbles) en un WAV segmentado.

Uso:
    python tone_nibbles.py coro.wav --segments 30 \
        --low 520 --high 1400 --step 40 --out work/
    python tone_nibbles.py coro.wav --segment-seconds 0.35 --low 520 --high 1400
    python tone_nibbles.py coro.wav --auto          # detecta picos por segmento

Cada segmento se analiza con FFT (ventana Hann). Se busca un pico en la banda grave
(nibble alto) y otro en la aguda (nibble bajo): byte = (alto<<4) | bajo.
Requiere numpy.
"""
from __future__ import annotations

import argparse
import sys
import wave

try:
    import numpy as np
except ImportError:
    sys.exit("falta numpy: pip install numpy")


def cargar(ruta: str) -> tuple[np.ndarray, int]:
    with wave.open(ruta, "rb") as w:
        sr = w.getframerate()
        canales = w.getnchannels()
        sw = w.getsampwidth()
        datos = w.readframes(w.getnframes())
    dtype = {1: np.uint8, 2: "<i2", 4: "<i4"}.get(sw)
    if dtype is None:
        sys.exit(f"ancho de muestra no soportado: {sw}")
    arr = np.frombuffer(datos, dtype=dtype).astype(np.float64)
    if canales > 1:
        arr = arr.reshape(-1, canales)[:, 0]
    return arr, sr


def pico(seg: np.ndarray, sr: int, fmin: float, fmax: float) -> tuple[float, float]:
    n = 1 << 15
    if len(seg) < n:
        seg = np.pad(seg, (0, n - len(seg)))
    else:
        seg = seg[:n]
    ventana = np.hanning(len(seg))
    espectro = np.abs(np.fft.rfft(seg * ventana))
    freqs = np.fft.rfftfreq(len(seg), 1 / sr)
    mascara = (freqs >= fmin) & (freqs <= fmax)
    if not mascara.any():
        return 0.0, 0.0
    idx = np.argmax(espectro[mascara])
    f = float(freqs[mascara][idx])
    return f, float(espectro[mascara][idx])


def indices(f: float, base: float, paso: float) -> int:
    return int(round((f - base) / paso))


def main() -> int:
    ap = argparse.ArgumentParser(description="Tonos duales → bytes")
    ap.add_argument("audio")
    ap.add_argument("--low", type=float, default=480.0, help="base banda grave")
    ap.add_argument("--high", type=float, default=1320.0, help="base banda aguda")
    ap.add_argument("--step", type=float, default=40.0)
    ap.add_argument("--segments", type=int)
    ap.add_argument("--segment-seconds", type=float)
    ap.add_argument("--auto", action="store_true")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    data, sr = cargar(args.audio)
    print(f"audio: {len(data)} muestras @ {sr} Hz "
          f"({len(data)/sr:.3f} s)")

    if args.auto:
        # Segmentación por energía: detecta regiones activas
        ventana = int(sr * 0.01)
        energia = np.array([np.abs(data[i:i + ventana]).mean()
                            for i in range(0, len(data) - ventana, ventana)])
        umbral = energia.max() * 0.15
        activo = energia > umbral
        segmentos, ini = [], None
        for i, a in enumerate(activo):
            if a and ini is None:
                ini = i
            elif not a and ini is not None:
                if (i - ini) * ventana > sr * 0.1:
                    segmentos.append((ini * ventana, i * ventana))
                ini = None
        if ini is not None:
            segmentos.append((ini * ventana, len(data)))
        print(f"segmentos detectados: {len(segmentos)}")
    else:
        seg_s = args.segment_seconds or (
            len(data) / sr / args.segments if args.segments else len(data) / sr)
        n = args.segments or int(round(len(data) / sr / seg_s))
        largo = int(sr * seg_s)
        segmentos = [(i * largo, min((i + 1) * largo, len(data))) for i in range(n)]
        print(f"segmentos fijos: {len(segmentos)} de {seg_s:.3f} s")

    # Ventana interna: 15 % … 80 % del segmento (evita ataques y colas)
    filas, salida = [], bytearray()
    for i, (a, b) in enumerate(segmentos):
        ini = a + int((b - a) * 0.15)
        fin = a + int((b - a) * 0.80)
        seg = data[ini:fin]
        f_bajo, _ = pico(seg, sr, args.low, args.low + args.step * 16)
        f_alto, _ = pico(seg, sr, args.high, args.high + args.step * 16)
        k_bajo = indices(f_bajo, args.low, args.step)
        k_alto = indices(f_alto, args.high, args.step)
        valido = 0 <= k_alto <= 15
        byte = (k_alto << 4) | (k_bajo & 0xF) if valido else None
        filas.append((i + 1, f_bajo, k_bajo, f_alto, k_alto, byte))
        if byte is not None:
            salida.append(byte)

    print(f"\n{'seg':>4} {'f_bajo':>8} {'k':>3} {'f_alto':>8} {'k':>3}  byte")
    for f in filas:
        print(f"{f[0]:>4} {f[1]:>8.1f} {f[2]:>3} {f[3]:>8.1f} {f[4]:>3}  "
              f"{'-' if f[5] is None else f'0x{f[5]:02x} {chr(f[5]) if 32 <= f[5] < 127 else '.'}'}")

    texto = bytes(salida)
    print(f"\nbytes: {texto.hex()}")
    print(f"ascii: {texto.decode('latin-1')}")
    if args.out:
        with open(args.out, "wb") as fh:
            fh.write(texto)
        print(f"guardado: {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
