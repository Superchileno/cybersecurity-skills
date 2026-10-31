#!/usr/bin/env python3
"""Crib-dragging: recupera keystream con un fragmento de texto plano esperado.

Uso:
    python crib_drag.py cifrado.bin --crib "flag{"
    python crib_drag.py cifrado.hex --hex --crib "flag{" --max-key 64
    python crib_drag.py cifrado.bin --crib "usuario=" --report

Salida: candidatos de keystream y, si se detecta periodicidad, la clave.
"""
from __future__ import annotations

import argparse
import binascii
import string
import sys

IMPRIMIBLES = set(bytes(string.printable, "ascii"))


def leer(ruta: str, hexa: bool) -> bytes:
    with open(ruta, "rb") as fh:
        data = fh.read()
    if hexa or ruta.endswith(".hex"):
        return binascii.unhexlify(b"".join(data.split()))
    return data


def puntuar(data: bytes) -> float:
    return sum(1 for b in data if b in IMPRIMIBLES) / max(1, len(data))


def periodo(ks: bytes, maximo: int) -> int | None:
    """Busca el periodo más pequeño que explica el keystream completo."""
    for p in range(1, min(maximo, len(ks)) + 1):
        if all(ks[i] == ks[i % p] for i in range(len(ks))):
            return p
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Crib-dragging")
    ap.add_argument("archivo")
    ap.add_argument("--crib", required=True)
    ap.add_argument("--hex", action="store_true")
    ap.add_argument("--max-key", type=int, default=64)
    ap.add_argument("--report", action="store_true",
                    help="descifrar el mensaje completo con cada candidato")
    ap.add_argument("--top", type=int, default=5)
    args = ap.parse_args()

    data = leer(args.archivo, args.hex)
    crib = args.crib.encode()
    print(f"cifrado: {len(data)} B | crib: {crib!r} ({len(crib)} B)")

    candidatos = []
    for offset in range(0, len(data) - len(crib) + 1):
        ks = bytes(c ^ p for c, p in zip(data[offset:offset + len(crib)], crib))
        # Un keystream "razonable" suele ser imprimible o de bytes bajos
        score = puntuar(ks)
        candidatos.append((score, offset, ks))

    candidatos.sort(key=lambda t: (-t[0], t[1]))
    for score, offset, ks in candidatos[:args.top]:
        p = periodo(ks, args.max_key)
        print(f"\noffset 0x{offset:x} ({offset}): keystream={ks.hex()} "
              f"imprimible={score:.0%} periodo={p}")

        if p:
            clave = ks[:p]
            print(f"  [+] clave candidata ({p} B): {clave!r}")
            if args.report:
                plano = bytes(c ^ clave[i % p] for i, c in enumerate(data))
                print(f"  descifrado ({puntuar(plano):.0%}):")
                print("   ", plano.decode("latin-1").replace("\r", "")[:400])

        if args.report and not p:
            plano = bytes(c ^ ks[i % len(ks)] for i, c in enumerate(data))
            print(f"  intento con keystream de {len(ks)} B "
                  f"({puntuar(plano):.0%}):")
            print("   ", plano.decode("latin-1").replace("\r", "")[:400])

    return 0


if __name__ == "__main__":
    sys.exit(main())
