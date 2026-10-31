#!/usr/bin/env python3
"""Extrae datos anexados después del fin lógico de un archivo (polyglot / carving).

Uso:
    python carve_appended.py reto.png --out work/
    python carve_appended.py reto.jpg --out work/ --dry-run
    python carve_appended.py reto.png --out work/ --min-bytes 16

Soporta PNG (IEND), JPEG (EOI), GIF (0x3B), PDF (%%EOF), ZIP (fin de directorio)
y RIFF/WAV (tamaño declarado). Si la cola es un ZIP, la lista y la extrae.
"""
from __future__ import annotations

import argparse
import io
import os
import sys
import zipfile


def fin_logico(data: bytes) -> tuple[int | None, str]:
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        pos = data.rfind(b"IEND")
        if pos == -1:
            return None, "PNG sin IEND"
        return pos + 8, "PNG/IEND"
    if data.startswith(b"\xff\xd8\xff"):
        pos = data.rfind(b"\xff\xd9")
        return (pos + 2, "JPEG/EOI") if pos != -1 else (None, "JPEG sin EOI")
    if data.startswith((b"GIF89a", b"GIF87a")):
        pos = data.rfind(b"\x3b")
        return (pos + 1, "GIF/trailer") if pos != -1 else (None, "GIF sin trailer")
    if data.startswith(b"%PDF"):
        pos = data.rfind(b"%%EOF")
        return (pos + 5, "PDF/%%EOF") if pos != -1 else (None, "PDF sin EOF")
    if data.startswith(b"PK\x03\x04"):
        pos = data.rfind(b"PK\x05\x06")
        if pos == -1:
            return None, "ZIP sin directorio central"
        comentario = int.from_bytes(data[pos + 20:pos + 22], "little")
        return pos + 22 + comentario, "ZIP/EOCD"
    if data.startswith(b"RIFF") and len(data) >= 8:
        tam = int.from_bytes(data[4:8], "little")
        return min(8 + tam, len(data)), "RIFF/size"
    return None, "formato no reconocido"


def extraer_zip(cola: bytes, base: str, destino: str) -> None:
    inicio = cola.find(b"PK\x03\x04")
    if inicio == -1:
        print("  [!] la firma PK no está en la cola")
        return
    blob = cola[inicio:]
    try:
        zf = zipfile.ZipFile(io.BytesIO(blob))
    except zipfile.BadZipFile as exc:
        print(f"  [!] ZIP inválido: {exc} (probando recorte final)")
        # Algunos retos dejan basura después del EOCD
        eocd = blob.rfind(b"PK\x05\x06")
        if eocd == -1:
            return
        comentario = int.from_bytes(blob[eocd + 20:eocd + 22], "little")
        zf = zipfile.ZipFile(io.BytesIO(blob[:eocd + 22 + comentario]))
    print(f"  ZIP anexado en offset 0x{inicio:x} ({len(blob)} bytes)")
    for info in zf.infolist():
        print(f"    - {info.filename:<40} {info.file_size:>10} B "
              f"{'cifrado' if info.flag_bits & 0x1 else ''}")
    out = os.path.join(destino, base + "_anexado")
    zf.extractall(out)
    print(f"  extraído en: {out}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Carving de datos anexados")
    ap.add_argument("archivo")
    ap.add_argument("--out", default="work")
    ap.add_argument("--min-bytes", type=int, default=8,
                    help="mínimo de bytes tras el fin para considerarlo payload")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    with open(args.archivo, "rb") as fh:
        data = fh.read()

    fin, tipo = fin_logico(data)
    print(f"archivo : {args.archivo} ({len(data)} B)")
    print(f"formato : {tipo}")
    if fin is None:
        print("[!] no se pudo determinar el fin lógico; busca firmas manualmente")
        return 1
    print(f"fin     : 0x{fin:x}")
    resto = data[fin:]
    print(f"cola    : {len(resto)} bytes")
    if len(resto) < args.min_bytes:
        print("[i] no hay payload anexado relevante")
        return 0
    print(f"primeros: {resto[:24].hex(' ')}")

    if args.dry_run:
        return 0

    os.makedirs(args.out, exist_ok=True)
    base = os.path.splitext(os.path.basename(args.archivo))[0]
    if resto[:2] == b"PK" or resto.find(b"PK\x03\x04") != -1:
        extraer_zip(resto, base, args.out)
    else:
        ruta = os.path.join(args.out, base + "_cola.bin")
        with open(ruta, "wb") as fh:
            fh.write(resto)
        print(f"  guardado en: {ruta}")

    # Informar de otras firmas presentes en la cola
    firmas = {
        b"\x1f\x8b": "gzip",
        b"BZh": "bzip2",
        b"\xfd7zXZ": "xz",
        b"\x89PNG": "png",
        b"\xff\xd8\xff": "jpeg",
        b"7z\xbc\xaf": "7z",
        b"Rar!": "rar",
    }
    for firma, nombre in firmas.items():
        pos = resto.find(firma)
        if pos != -1:
            print(f"  [!] firma {nombre} en la cola, offset +0x{pos:x}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
