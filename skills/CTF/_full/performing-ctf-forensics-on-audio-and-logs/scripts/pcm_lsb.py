#!/usr/bin/env python3
"""Extrae el LSB de las muestras de un WAV (bit 0 por defecto).

Uso:
    python pcm_lsb.py audio.wav --bit 0 --msb-first
    python pcm_lsb.py audio.wav --bit 0 --xor CLAVE
    python pcm_lsb.py audio.wav --bit 1 --channels 0 --out work/lsb.bin

Requiere numpy.
"""
from __future__ import annotations

import argparse
import base64
import sys
import wave

try:
    import numpy as np
except ImportError:
    sys.exit("falta numpy: pip install numpy")


def cargar(ruta: str) -> tuple[np.ndarray, int, int, int]:
    with wave.open(ruta, "rb") as w:
        sr, canales, sw = w.getframerate(), w.getnchannels(), w.getsampwidth()
        datos = w.readframes(w.getnframes())
    dtype = {1: np.uint8, 2: "<i2", 4: "<i4"}.get(sw)
    if dtype is None:
        sys.exit(f"ancho de muestra no soportado: {sw}")
    arr = np.frombuffer(datos, dtype=dtype)
    if canales > 1:
        arr = arr.reshape(-1, canales)
    return arr, sr, canales, sw


def main() -> int:
    ap = argparse.ArgumentParser(description="LSB de muestras PCM")
    ap.add_argument("audio")
    ap.add_argument("--bit", type=int, default=0, choices=range(0, 8))
    ap.add_argument("--msb-first", action="store_true", default=True)
    ap.add_argument("--lsb-first", dest="msb_first", action="store_false")
    ap.add_argument("--channels", type=int, default=None,
                    help="índice de canal (por defecto todos, intercalados)")
    ap.add_argument("--xor", help="clave para XOR con el resultado")
    ap.add_argument("--out")
    ap.add_argument("--max-bytes", type=int, default=4096)
    args = ap.parse_args()

    arr, sr, canales, sw = cargar(args.audio)
    print(f"audio: {sr} Hz, {canales} canal(es), {sw*8} bits, "
          f"{arr.shape[0]} muestras")

    if canales > 1 and args.channels is not None:
        muestras = arr[:, args.channels]
    else:
        muestras = arr.reshape(-1)

    bits = ((muestras >> args.bit) & 1).astype(np.uint8)
    paquete = np.packbits(bits, bitorder="big" if args.msb_first else "little")
    datos = paquete.tobytes()

    # Cortar en el primer NUL si el contenido parece texto
    pos = datos.find(b"\x00")
    if 0 < pos < len(datos):
        print(f"[i] terminador NUL en {pos}")
        datos = datos[:pos]

    if args.xor:
        clave = args.xor.encode()
        datos = bytes(b ^ clave[i % len(clave)] for i, b in enumerate(datos))
        print(f"[i] XOR con {args.xor!r}")

    ratio = sum(1 for b in datos if 32 <= b < 127) / max(1, len(datos))
    print(f"resultado: {len(datos)} B, {ratio:.0%} imprimible")
    muestra = datos[:args.max_bytes]
    print("---")
    print(muestra.decode("latin-1"))

    # Intentar Base64 si el alfabeto encaja
    alfabeto = set(b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=")
    if set(muestra[:200]).issubset(alfabeto):
        print("\n[i] alfabeto Base64 detectado, probando decodificación:")
        try:
            dec = base64.b64decode(datos + b"=" * (-len(datos) % 4))
            print(dec.decode("latin-1")[:400])
        except Exception as exc:  # noqa: BLE001
            print(f"    fallo: {exc}")

    if args.out:
        with open(args.out, "wb") as fh:
            fh.write(datos)
        print(f"\nguardado: {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
