#!/usr/bin/env python3
"""Vigenère / César con variantes de CTF.

Uso:
    # Descifrar probando ambos signos y reportar el más legible
    python vigenere.py --input cifrado.txt --key COLINA --crib PREFIJO

    # Forzar el signo inverso
    python vigenere.py --input cifrado.txt --key COLINA --invert

    # La clave sólo avanza en letras (por defecto) o en todos los caracteres
    python vigenere.py --input cifrado.txt --key COLINA --advance all

    # César: probar los 26 desplazamientos
    python vigenere.py --caesar --input cifrado.txt --crib PREFIJO
"""
from __future__ import annotations

import argparse
import sys

FRECUENCIA = {" ": 0.18, "e": 0.13, "a": 0.12, "o": 0.09, "s": 0.08,
              "r": 0.07, "n": 0.07, "i": 0.06, "d": 0.06, "l": 0.05}


def vigenere(texto: str, clave: str, signo: int = 1, avanzar: str = "letras") -> str:
    salida = []
    k = 0
    for ch in texto:
        if ch.isascii() and ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            desplaz = ord(clave[k % len(clave)].lower()) - ord("a")
            salida.append(chr((ord(ch) - base + signo * desplaz) % 26 + base))
            k += 1
        else:
            salida.append(ch)
            if avanzar == "all":
                k += 1
    return "".join(salida)


def puntuar(texto: str) -> float:
    texto = texto.lower()
    if not texto:
        return 0.0
    return sum(FRECUENCIA.get(c, 0) for c in texto) / len(texto)


def caesar(texto: str, desplaz: int) -> str:
    salida = []
    for ch in texto:
        if ch.isascii() and ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            salida.append(chr((ord(ch) - base + desplaz) % 26 + base))
        else:
            salida.append(ch)
    return "".join(salida)


def main() -> int:
    ap = argparse.ArgumentParser(description="Vigenère / César")
    ap.add_argument("--input", required=True)
    ap.add_argument("--key")
    ap.add_argument("--invert", action="store_true")
    ap.add_argument("--advance", choices=["letras", "all"], default="letras")
    ap.add_argument("--crib", help="prefijo esperado, p.ej. PREFIJO")
    ap.add_argument("--caesar", action="store_true")
    ap.add_argument("--all", action="store_true", help="mostrar todos los candidatos")
    args = ap.parse_args()

    with open(args.input, "r", encoding="latin-1") as fh:
        texto = fh.read()

    if args.caesar:
        resultados = []
        for d in range(26):
            cand = caesar(texto, d)
            resultados.append((puntuar(cand), d, cand))
        resultados.sort(reverse=True)
        for score, d, cand in (resultados if args.all else resultados[:5]):
            marca = " <<<" if args.crib and args.crib in cand else ""
            print(f"\n[desplazamiento {d:+d}] score={score:.3f}{marca}")
            print(cand[:300])
        return 0

    if not args.key:
        print("[!] se requiere --key (o usa --caesar)")
        return 1

    combinaciones = [(-1, "invertido")] if args.invert else [(1, "directo"), (-1, "invertido")]
    for signo, nombre in combinaciones:
        cand = vigenere(texto, args.key, signo, args.advance)
        score = puntuar(cand)
        marca = " <<< crib encontrado" if args.crib and args.crib in cand else ""
        print(f"\n[modo {nombre}, avance={args.advance}] score={score:.3f}{marca}")
        print(cand[:400])
    return 0


if __name__ == "__main__":
    sys.exit(main())
