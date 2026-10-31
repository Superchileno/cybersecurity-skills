#!/usr/bin/env python3
"""Extrae y clasifica tablas de bytes desde un ELF (o desde un volcado hex).

Uso:
    python extract_tables.py ./binario --offset 0x21a0 --length 32
    python extract_tables.py ./binario --section .rodata --scan
    python extract_tables.py --hex "0301040200" --classify

Clasifica:
    - catálogo de nibbles (16 valores 0..15)
    - permutación (0..n-1 sin repetidos)
    - clave XOR (bytes altos)
    - array de direcciones (8 B, dentro de .text)
"""
from __future__ import annotations

import argparse
import binascii
import sys

try:
    from elftools.elf.elffile import ELFFile
except ImportError:
    ELFFile = None


def leer_elf(ruta: str, seccion: str | None, offset: int | None,
             largo: int) -> tuple[bytes, int]:
    if ELFFile is None:
        sys.exit("falta pyelftools: pip install pyelftools")
    with open(ruta, "rb") as fh:
        elf = ELFFile(fh)
        if offset is not None:
            # offset virtual -> offset de archivo
            for s in elf.iter_sections():
                a, o, sz = s["sh_addr"], s["sh_offset"], s["sh_size"]
                if a <= offset < a + sz:
                    fh.seek(o + (offset - a))
                    return fh.read(largo), offset
            fh.seek(offset)
            return fh.read(largo), offset
        sec = elf.get_section_by_name(seccion or ".rodata")
        if sec is None:
            sys.exit(f"sección no encontrada: {seccion}")
        return sec.data()[:largo or sec.data_size], sec["sh_addr"]


def clasificar(data: bytes) -> list[str]:
    etiquetas = []
    n = len(data)
    if n == 16 and sorted(data) == list(range(16)):
        etiquetas.append("catálogo de nibbles (permutación 0..15)")
    if sorted(data) == list(range(n)):
        etiquetas.append(f"permutación de índices (0..{n-1})")
    if n % 8 == 0 and n >= 16:
        valores = [int.from_bytes(data[i:i + 8], "little") for i in range(0, n, 8)]
        if all(v > 0x400000 for v in valores):
            etiquetas.append("posible array de punteros (tabla de saltos)")
    imprimibles = sum(1 for b in data if 32 <= b < 127)
    if imprimibles / max(1, n) > 0.85:
        etiquetas.append("texto ASCII")
    elif imprimibles / max(1, n) < 0.2:
        etiquetas.append("datos binarios / posible clave XOR")
    return etiquetas or ["sin clasificación clara"]


def main() -> int:
    ap = argparse.ArgumentParser(description="Extrae tablas")
    ap.add_argument("binario", nargs="?")
    ap.add_argument("--offset", help="dirección virtual (hex)")
    ap.add_argument("--section", default=".rodata")
    ap.add_argument("--length", type=int, default=64)
    ap.add_argument("--hex", help="volcado hex directo (sin binario)")
    ap.add_argument("--classify", action="store_true")
    args = ap.parse_args()

    if args.hex:
        data = binascii.unhexlify("".join(args.hex.split()))
        base = 0
    elif args.binario:
        offset = int(args.offset, 16) if args.offset else None
        data, base = leer_elf(args.binario, args.section, offset, args.length)
    else:
        print("[!] indica un binario o --hex")
        return 1

    print(f"base: 0x{base:x}, {len(data)} B")
    for i in range(0, len(data), 16):
        trozo = data[i:i + 16]
        hexa = " ".join(f"{b:02x}" for b in trozo)
        ascii_ = "".join(chr(b) if 32 <= b < 127 else "." for b in trozo)
        print(f"{base + i:08x}  {hexa:<47}  |{ascii_}|")

    print("\nbytes:", list(data))
    if args.classify or True:
        print("clasificación:")
        for e in clasificar(data):
            print(f"  - {e}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
