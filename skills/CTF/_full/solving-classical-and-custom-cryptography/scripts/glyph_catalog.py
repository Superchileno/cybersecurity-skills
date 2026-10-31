#!/usr/bin/env python3
"""Decodifica láminas de glifos usando un catálogo (2 glifos por byte, hex).

Uso:
    # Validar primero con la lámina de control
    python glyph_catalog.py --catalog catalogo.txt --lamina control.txt \
        --expect "ENSAYO DE IMPRENTA"

    # Decodificar el objetivo con el catálogo validado
    python glyph_catalog.py --catalog catalogo.txt --lamina objetivo.txt

Formato del catálogo (flexible): cada línea con un glifo y su valor hex,
separados por espacio, coma, tab o ':'. Ejemplo:

    ▽ 0
    ▲ 1
    ◇ 2
    ...
"""
from __future__ import annotations

import argparse
import re
import sys


def leer_catalogo(ruta: str) -> dict[str, int]:
    mapa: dict[str, int] = {}
    with open(ruta, "r", encoding="utf-8") as fh:
        for linea in fh:
            linea = linea.strip()
            if not linea or linea.startswith("#"):
                continue
            partes = re.split(r"[\s,:;=\t]+", linea, maxsplit=1)
            if len(partes) != 2:
                continue
            glifo, valor = partes[0], partes[1].strip()
            try:
                mapa[glifo] = int(valor, 16)
            except ValueError:
                continue
    return mapa


def decodificar(lamina: str, mapa: dict[str, int]) -> bytes:
    valores = []
    for ch in lamina:
        if ch in mapa:
            valores.append(mapa[ch])
        elif ch.isspace():
            continue
        else:
            print(f"[!] glifo sin mapeo: {ch!r} (U+{ord(ch):04X})")
    # 2 glifos por byte: el primero es el nibble alto
    salida = bytearray()
    for i in range(0, len(valores) - 1, 2):
        salida.append((valores[i] << 4) | valores[i + 1])
    return bytes(salida)


def main() -> int:
    ap = argparse.ArgumentParser(description="Catálogo de glifos → bytes")
    ap.add_argument("--catalog", required=True)
    ap.add_argument("--lamina", required=True)
    ap.add_argument("--expect", help="texto esperado (lámina de control)")
    ap.add_argument("--swap", help="dos glifos a intercambiar, p.ej. '▽,▲'")
    ap.add_argument("--raw", action="store_true", help="volcar también hex")
    args = ap.parse_args()

    mapa = leer_catalogo(args.catalog)
    print(f"catálogo: {len(mapa)} glifos")
    if len(mapa) != 16:
        print(f"[i] se esperaban 16 nibbles, hay {len(mapa)}")

    if args.swap:
        a, b = [s.strip() for s in args.swap.split(",")]
        if a in mapa and b in mapa:
            mapa[a], mapa[b] = mapa[b], mapa[a]
            print(f"[i] intercambiados {a} ↔ {b}")

    with open(args.lamina, "r", encoding="utf-8") as fh:
        lamina = fh.read()

    datos = decodificar(lamina, mapa)
    if args.raw:
        print(f"hex: {datos.hex()}")
    texto = datos.decode("utf-8", "replace")
    print(f"\ntexto ({len(datos)} B):")
    print(texto)

    if args.expect:
        normal = lambda s: re.sub(r"\s+", " ", s.strip().upper())
        ok = normal(args.expect) in normal(texto)
        print(f"\n[{'✓' if ok else '✗'}] control esperado: "
              f"{'coincide' if ok else 'NO coincide → catálogo incorrecto'}")
        return 0 if ok else 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
