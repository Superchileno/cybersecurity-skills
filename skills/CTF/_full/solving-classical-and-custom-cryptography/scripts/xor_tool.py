#!/usr/bin/env python3
"""Herramienta XOR para CTF: clave simple, clave repetida y two-time pad.

Uso:
    # XOR con clave repetida sobre bytes (entrada hex o archivo)
    python xor_tool.py rep --input cifrado.hex --hex --key clave_de_ejemplo
    python xor_tool.py rep --input datos.bin --key "CE2RCA"

    # Par conocido: recupera keystream y descifra el objetivo
    python xor_tool.py known --plain mi_sesion.txt --cipher mi_token.hex \
        --target token_gerencia.hex

    # XOR entre dos cifrados (busca ceros = mismo keystream)
    python xor_tool.py diff --a t1.hex --b t2.hex

    # Fuerza bruta de clave de 1 byte
    python xor_tool.py brute --input datos.bin

Salida: texto en stdout y, con --out, binario en archivo.
"""
from __future__ import annotations

import argparse
import binascii
import string
import sys

IMPRIMIBLES = set(bytes(string.printable, "ascii"))


def leer(ruta: str | None, hexa: bool, texto: str | None) -> bytes:
    if texto is not None:
        return texto.encode()
    if ruta is None:
        return sys.stdin.buffer.read()
    with open(ruta, "rb") as fh:
        data = fh.read()
    if hexa or (ruta.endswith(".hex")):
        limpio = b"".join(data.split())
        return binascii.unhexlify(limpio)
    return data


def puntuar(data: bytes) -> float:
    if not data:
        return 0.0
    return sum(1 for b in data if b in IMPRIMIBLES) / len(data)


def xor_repetido(data: bytes, clave: bytes) -> bytes:
    if not clave:
        raise ValueError("clave vacía")
    return bytes(c ^ clave[i % len(clave)] for i, c in enumerate(data))


def mostrar(data: bytes, etiqueta: str) -> None:
    ratio = puntuar(data)
    print(f"{etiqueta}: {len(data)} B, imprimible {ratio:.0%}")
    print(data.decode("latin-1").replace("\r", ""))


def cmd_rep(args) -> int:
    data = leer(args.input, args.hex, None)
    clave = args.key.encode() if args.key else sys.stdin.buffer.readline().strip()
    salida = xor_repetido(data, clave)
    mostrar(salida, f"XOR con '{clave.decode('latin-1')}'")
    if args.out:
        with open(args.out, "wb") as fh:
            fh.write(salida)
    return 0


def cmd_known(args) -> int:
    plano = leer(args.plain, False, None)
    c1 = leer(args.cipher, True, None)
    c2 = leer(args.target, True, None)
    if len(plano) != len(c1):
        print(f"[!] el par conocido no coincide: {len(plano)} vs {len(c1)}")
        return 1
    keystream = bytes(p ^ c for p, c in zip(plano, c1))
    print(f"keystream ({len(keystream)} B): {keystream.hex()}")
    if len(keystream) >= 8:
        print(f"  primeros 8: {keystream[:8].hex()}  últimos 8: {keystream[-8:].hex()}")
        if keystream[:8] == keystream[-8:]:
            print("  [i] repetición en los extremos: posible clave de 8 bytes")
    salida = bytes(c ^ keystream[i % len(keystream)] for i, c in enumerate(c2))
    mostrar(salida, "objetivo descifrado")
    if args.out:
        with open(args.out, "wb") as fh:
            fh.write(salida)
    return 0


def cmd_diff(args) -> int:
    a = leer(args.a, True, None)
    b = leer(args.b, True, None)
    n = min(len(a), len(b))
    dif = bytes(x ^ y for x, y in zip(a[:n], b[:n]))
    print(f"longitudes: {len(a)} / {len(b)}; comparando {n} B")
    ceros_ini = next((i for i, v in enumerate(dif) if v), n)
    ceros_fin = next((i for i, v in enumerate(reversed(dif)) if v), n)
    print(f"  ceros al inicio: {ceros_ini}  al final: {ceros_fin}")
    if ceros_ini or ceros_fin:
        print("  [i] extremos nulos → probable mismo keystream (usa 'known')")
    mostrar(dif, "A ⊕ B")
    return 0


def cmd_brute(args) -> int:
    data = leer(args.input, args.hex, None)
    resultados = []
    for k in range(256):
        cand = bytes(b ^ k for b in data)
        resultados.append((puntuar(cand), k, cand))
    resultados.sort(reverse=True)
    for ratio, k, cand in resultados[:5]:
        print(f"\nclave 0x{k:02x} ({ratio:.0%} imprimible)")
        print(cand.decode("latin-1").replace("\r", "")[:300])
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="XOR para CTF")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("rep")
    p.add_argument("--input", required=True)
    p.add_argument("--hex", action="store_true")
    p.add_argument("--key", required=True)
    p.add_argument("--out")
    p.set_defaults(func=cmd_rep)

    p = sub.add_parser("known")
    p.add_argument("--plain", required=True)
    p.add_argument("--cipher", required=True)
    p.add_argument("--target", required=True)
    p.add_argument("--out")
    p.set_defaults(func=cmd_known)

    p = sub.add_parser("diff")
    p.add_argument("--a", required=True)
    p.add_argument("--b", required=True)
    p.set_defaults(func=cmd_diff)

    p = sub.add_parser("brute")
    p.add_argument("--input", required=True)
    p.add_argument("--hex", action="store_true")
    p.set_defaults(func=cmd_brute)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
