#!/usr/bin/env python3
"""Extrae el LSB de una imagen con parámetros configurables.

Uso:
    python lsb_extract.py reto.png --bit 0 --order interleaved
    python lsb_extract.py reto.png --bit 1 --order planar --channel 0 --out work/lsb.txt
    python lsb_extract.py reto.png --bit 0 --stop-at-nul
    python lsb_extract.py reto.png --bit 0 --auto      # prueba 0..3 y reporta

Requiere Pillow. Opcional numpy (más rápido).
"""
from __future__ import annotations

import argparse
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("falta Pillow: pip install pillow")


def bits_de_imagen(img: Image.Image, bit: int, orden: str, canal: int | None):
    img = img.convert("RGB")
    w, h = img.size
    px = img.load()
    bits: list[int] = []
    if orden == "interleaved":
        for y in range(h):
            for x in range(w):
                pixel = px[x, y]
                if canal is None:
                    for c in range(3):
                        bits.append((pixel[c] >> bit) & 1)
                else:
                    bits.append((pixel[canal] >> bit) & 1)
    elif orden == "planar":
        canales = range(3) if canal is None else [canal]
        for c in canales:
            for y in range(h):
                for x in range(w):
                    bits.append((px[x, y][c] >> bit) & 1)
    else:
        raise ValueError(f"orden desconocido: {orden}")
    return bits


def bits_a_bytes(bits: list[int]) -> bytes:
    salida = bytearray()
    for i in range(0, len(bits) - 7, 8):
        byte = 0
        for k in range(8):
            byte = (byte << 1) | bits[i + k]
        salida.append(byte)
    return bytes(salida)


def imprimible(data: bytes) -> float:
    if not data:
        return 0.0
    ok = sum(1 for b in data if 32 <= b < 127 or b in (9, 10, 13))
    return ok / len(data)


def resumir(data: bytes, etiqueta: str) -> None:
    ratio = imprimible(data)
    muestra = data[:96].decode("latin-1", "replace").replace("\n", "\\n")
    print(f"{etiqueta}: {len(data)} B, imprimible {ratio:.0%}")
    print(f"   {muestra}")
    if ratio > 0.85:
        print("   >>> texto plano, revisar")
    # ¿parece Base64?
    alfabeto = set(b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=")
    if data and set(data[:200]).issubset(alfabeto):
        print("   >>> alfabeto Base64, probar decodificación")


def main() -> int:
    ap = argparse.ArgumentParser(description="Extracción LSB")
    ap.add_argument("imagen")
    ap.add_argument("--bit", type=int, default=0, choices=range(0, 4))
    ap.add_argument("--order", default="interleaved",
                    choices=["interleaved", "planar"])
    ap.add_argument("--channel", type=int, default=None, choices=[0, 1, 2],
                    help="0=R, 1=G, 2=B (por defecto los tres)")
    ap.add_argument("--stop-at-nul", action="store_true")
    ap.add_argument("--auto", action="store_true", help="prueba bits 0..3")
    ap.add_argument("--out")
    args = ap.parse_args()

    img = Image.open(args.imagen)
    print(f"imagen: {args.imagen} {img.size[0]}x{img.size[1]} {img.mode}")

    if args.auto:
        for bit in range(4):
            datos = bits_a_bytes(bits_de_imagen(img, bit, args.order, args.channel))
            resumir(datos, f"bit {bit}/{args.order}")
        return 0

    datos = bits_a_bytes(bits_de_imagen(img, args.bit, args.order, args.channel))
    if args.stop_at_nul:
        pos = datos.find(b"\x00")
        if pos != -1:
            datos = datos[:pos]
            print(f"[i] truncado en NUL (offset {pos})")

    resumir(datos, f"bit {args.bit}/{args.order}/canal={args.channel}")

    if args.out:
        with open(args.out, "wb") as fh:
            fh.write(datos)
        print(f"guardado: {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
