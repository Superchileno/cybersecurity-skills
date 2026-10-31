#!/usr/bin/env python3
"""Decodificador en cadena: prueba automáticamente capas de codificación.

Uso:
    python decode_chain.py --text "$(cat mensaje.txt)"
    python decode_chain.py --file mensaje.txt --max-depth 8
    python decode_chain.py --file capa.txt --flag-prefix PREFIJO --verbose

En cada nivel intenta: hex, Base64, Base64url, Base32, ASCII85, Base45, URL-encode,
gzip/zlib/deflate, ROT13 y reverso de cadena. Se detiene cuando:
  - aparece el prefijo de flag, o
  - el texto deja de "mejorar" (no reduce tamaño ni aumenta imprimibilidad).
"""
from __future__ import annotations

import argparse
import base64
import binascii
import codecs
import gzip
import re
import sys
import urllib.parse
import zlib

try:
    import base45  # pip install base45
except ImportError:
    base45 = None

RE_HEX = re.compile(r"^[0-9a-fA-F\s]+$")
RE_B64 = re.compile(r"^[A-Za-z0-9+/=\s]+$")
RE_B64URL = re.compile(r"^[A-Za-z0-9\-_=\s]+$")
RE_B32 = re.compile(r"^[A-Z2-7=\s]+$")


def imprimible(texto: str) -> float:
    if not texto:
        return 0.0
    ok = sum(1 for c in texto if c.isprintable() or c in "\n\r\t")
    return ok / len(texto)


def intentar(nombre: str, fn, texto: str) -> tuple[str, bytes] | None:
    try:
        out = fn(texto)
    except Exception:  # noqa: BLE001
        return None
    if out is None:
        return None
    if isinstance(out, bytes):
        try:
            return nombre, out.decode("utf-8")
        except UnicodeDecodeError:
            return None
    return nombre, out


def transformaciones(texto: str) -> list[tuple[str, str]]:
    t = texto.strip()
    candidatos: list[tuple[str, str]] = []

    def add(nombre, fn):
        r = intentar(nombre, fn, t)
        if r:
            candidatos.append(r)

    if len(t) % 2 == 0 and RE_HEX.match(t):
        add("hex", lambda s: bytes.fromhex("".join(s.split())))
    if len(t) % 4 == 0 and RE_B64.match(t) and any(c.isupper() for c in t):
        add("base64", lambda s: base64.b64decode("".join(s.split()), validate=True))
    if RE_B64URL.match(t) and "-" in t or "_" in t:
        add("base64url", lambda s: base64.urlsafe_b64decode(
            s + "=" * (-len(s) % 4)))
    if len(t) % 8 == 0 and RE_B32.match(t):
        add("base32", lambda s: base64.b32decode("".join(s.split())))
    if base45 and len(t) % 3 == 0:
        add("base45", lambda s: base45.b45decode("".join(s.split())))
    if "%" in t:
        add("url", lambda s: urllib.parse.unquote(s))
    add("rot13", lambda s: codecs.decode(s, "rot13"))
    add("reverso", lambda s: s[::-1])
    add("ascii85", lambda s: base64.a85decode(s))
    return candidatos


def descomprimir(data: bytes) -> tuple[str, bytes] | None:
    for nombre, fn in (("gzip", gzip.decompress), ("zlib", zlib.decompress),
                       ("deflate", lambda d: zlib.decompress(d, -15))):
        try:
            return nombre, fn(data)
        except Exception:  # noqa: BLE001
            continue
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Cadena de decodificación")
    ap.add_argument("--text")
    ap.add_argument("--file")
    ap.add_argument("--max-depth", type=int, default=8)
    ap.add_argument("--flag-prefix", default=None,
                    help="p.ej. PREFIJO o flag; se detiene al encontrarlo")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    if args.text is not None:
        actual = args.text
    elif args.file:
        with open(args.file, "r", encoding="latin-1") as fh:
            actual = fh.read()
    else:
        actual = sys.stdin.read()

    print(f"nivel 0: {len(actual)} chars, {imprimible(actual):.0%} imprimible")
    if args.verbose:
        print(f"  {actual[:160]}")

    for nivel in range(1, args.max_depth + 1):
        mejor = None
        mejor_score = -1.0
        for nombre, cand in transformaciones(actual):
            score = imprimible(cand) * 2 + (0.5 if len(cand) < len(actual) else 0)
            if args.verbose:
                print(f"  [cand] {nombre}: {len(cand)} chars, "
                      f"{imprimible(cand):.0%}, score {score:.2f}")
            if score > mejor_score:
                mejor_score, mejor = score, (nombre, cand)

        # Probar descompresión sobre los bytes del texto actual
        try:
            comp = descomprimir(actual.encode("latin-1"))
        except Exception:  # noqa: BLE001
            comp = None
        if comp:
            nombre, data = comp
            cand = data.decode("utf-8", "replace")
            score = imprimible(cand) * 2 + 1
            if score > mejor_score:
                mejor_score, mejor = score, (nombre, cand)

        if mejor is None:
            print("[i] no hay más transformaciones aplicables")
            break

        nombre, cand = mejor
        if len(cand) >= len(actual) and imprimible(cand) <= imprimible(actual):
            print(f"[i] '{nombre}' no mejora el resultado; se detiene")
            break

        actual = cand
        print(f"\nnivel {nivel}: {nombre} → {len(actual)} chars, "
              f"{imprimible(actual):.0%} imprimible")
        print("  ", actual[:300].replace("\n", "\\n"))

        if args.flag_prefix and args.flag_prefix in actual:
            print(f"\n[+] prefijo '{args.flag_prefix}' encontrado")
            idx = actual.index(args.flag_prefix)
            print("    ", actual[idx:idx + 200])
            break
        if "{" in actual and "}" in actual and len(actual) < 2000:
            print(f"\n[+] posible flag: {actual.strip()[:200]}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
