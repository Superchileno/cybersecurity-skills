#!/usr/bin/env python3
"""Triaje rápido de artefactos de CTF.

Uso:
    python ctf_triage.py archivo1 [archivo2 ...]
    python ctf_triage.py --hash reto.zip
    python ctf_triage.py --strings reto.png
    python ctf_triage.py --tail imagen.png      # busca datos tras el marcador de fin

No modifica nada: sólo lee y reporta. Pensado para Linux/macOS; en Windows
funciona igual salvo las herramientas externas que no existan.
"""
from __future__ import annotations

import argparse
import hashlib
import math
import os
import shutil
import subprocess
import sys
from collections import Counter

END_MARKERS = {
    b"\x89PNG\r\n\x1a\n": b"IEND",
    b"\xff\xd8\xff": b"\xff\xd9",          # JPEG EOI
    b"GIF89a": b"\x3b",
    b"GIF87a": b"\x3b",
    b"PK\x03\x04": b"PK\x05\x06",          # fin de directorio ZIP
    b"%PDF": b"%%EOF",
    b"RIFF": None,                          # WAV/AVI: tamaño en cabecera
}

MAGIC_HINTS = [
    (b"PK\x03\x04", "ZIP"),
    (b"\x89PNG", "PNG"),
    (b"\xff\xd8\xff", "JPEG"),
    (b"GIF8", "GIF"),
    (b"RIFF", "RIFF (WAV/AVI)"),
    (b"%PDF", "PDF"),
    (b"\x7fELF", "ELF"),
    (b"PK\x05\x06", "ZIP vacío"),
    (b"7z\xbc\xaf", "7-Zip"),
    (b"Rar!", "RAR"),
    (b"\x1f\x8b", "GZIP"),
    (b"BZh", "BZIP2"),
    (b"\xfd7zXZ", "XZ"),
    (b"OggS", "OGG"),
    (b"fLaC", "FLAC"),
    (b"ID3", "MP3"),
]


def entropia(data: bytes) -> float:
    if not data:
        return 0.0
    counts = Counter(data)
    total = len(data)
    return -sum((c / total) * math.log2(c / total) for c in counts.values())


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for bloque in iter(lambda: fh.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def magic(data: bytes) -> str:
    for firma, nombre in MAGIC_HINTS:
        if data.startswith(firma):
            return nombre
    return "desconocido"


def buscar_marcadores(data: bytes) -> list[str]:
    """Lista firmas conocidas y su offset, para detectar polyglots/anidados."""
    hallazgos = []
    for firma, nombre in MAGIC_HINTS:
        inicio = data.find(firma)
        while inicio != -1:
            hallazgos.append(f"{nombre} en offset 0x{inicio:x}")
            inicio = data.find(firma, inicio + 1)
            if len(hallazgos) > 40:
                return hallazgos + ["… (truncado)"]
    return hallazgos


def fin_aparente(data: bytes) -> int | None:
    for firma, marcador in END_MARKERS.items():
        if data.startswith(firma):
            if marcador is None:
                if len(data) >= 8:
                    return None
                continue
            if firma == b"\x89PNG\r\n\x1a\n":
                pos = data.rfind(b"IEND")
                return pos + 8 if pos != -1 else None
            pos = data.rfind(marcador)
            return pos + len(marcador) if pos != -1 else None
    return None


def herramientas() -> dict[str, bool]:
    nombres = ["file", "exiftool", "binwalk", "pngcheck", "foremost", "zbarimg", "sox"]
    return {n: bool(shutil.which(n)) for n in nombres}


def ejecutar(cmd: list[str], max_lineas: int = 25) -> str:
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        texto = (out.stdout or "") + (out.stderr or "")
        lineas = [l for l in texto.splitlines() if l.strip()]
        return "\n".join(lineas[:max_lineas])
    except Exception as exc:  # noqa: BLE001
        return f"[!] {cmd[0]}: {exc}"


def analizar(path: str, ver_strings: bool, ver_cola: bool) -> None:
    if not os.path.isfile(path):
        print(f"[!] no existe: {path}")
        return
    with open(path, "rb") as fh:
        data = fh.read()

    print("=" * 72)
    print(f"ARCHIVO: {path}")
    print(f"  tamaño   : {len(data)} bytes (0x{len(data):x})")
    print(f"  sha256   : {sha256(path)}")
    print(f"  magic    : {magic(data)}")
    print(f"  entropía : {entropia(data[:1 << 20]):.3f} bits/byte "
          f"(>7.5 ≈ cifrado/comprimido)")

    firmas = buscar_marcadores(data)
    if firmas:
        print("  firmas   :")
        for f in firmas:
            print(f"    - {f}")

    fin = fin_aparente(data)
    if fin is not None:
        resto = len(data) - fin
        print(f"  fin lógico: 0x{fin:x} → {resto} bytes después del marcador")
        if resto > 8:
            cola = data[fin:fin + 16]
            print(f"  cola      : {cola.hex(' ')}  ← posible polyglot/anidado")
            if fin + 4 <= len(data) and data[fin:fin + 2] == b"PK":
                print("              PK tras el fin: ZIP anexado (usa carve_appended.py)")

    if shutil.which("file"):
        print("  file     :", ejecutar(["file", "-b", path], 3))
    if shutil.which("exiftool"):
        print("  exiftool :")
        print(indentar(ejecutar(["exiftool", "-s", "-G1", path], 15)))
    if ver_strings:
        print("  strings  :")
        print(indentar(ejecutar(["strings", "-n", "6", path], 25)))
    if ver_cola:
        print("  últimas 128 bytes:")
        print(indentar(hexdump(data[-128:])))


def indentar(texto: str) -> str:
    return "\n".join("    " + l for l in texto.splitlines())


def hexdump(data: bytes) -> str:
    lineas = []
    for i in range(0, len(data), 16):
        trozo = data[i:i + 16]
        hexa = " ".join(f"{b:02x}" for b in trozo)
        ascii_ = "".join(chr(b) if 32 <= b < 127 else "." for b in trozo)
        lineas.append(f"{i:08x}  {hexa:<47}  |{ascii_}|")
    return "\n".join(lineas)


def main() -> int:
    ap = argparse.ArgumentParser(description="Triaje de artefactos CTF")
    ap.add_argument("archivos", nargs="+")
    ap.add_argument("--hash", action="store_true", help="sólo hash y tamaño")
    ap.add_argument("--strings", action="store_true", help="incluir strings")
    ap.add_argument("--tail", action="store_true", help="volcar los últimos 128 bytes")
    args = ap.parse_args()

    if not args.hash:
        disp = herramientas()
        faltan = [n for n, ok in disp.items() if not ok]
        if faltan:
            print(f"[i] herramientas no disponibles: {', '.join(faltan)}\n")

    for path in args.archivos:
        if args.hash:
            if os.path.isfile(path):
                print(f"{sha256(path)}  {os.path.getsize(path):>10}  {path}")
        else:
            analizar(path, args.strings, args.tail)
    return 0


if __name__ == "__main__":
    sys.exit(main())
