#!/usr/bin/env python3
"""Desanida ZIPs recursivamente en memoria (útil para retos de capas).

Uso:
    python zip_nested.py reto.zip --out work/capas
    python zip_nested.py reto.zip --out work/capas --max-depth 200

Detecta:
  - ZIP dentro de ZIP (por firma, aunque la extensión no lo diga)
  - archivos cifrados (se detiene y lo reporta)
  - nombres que colisionan (F(1)=F(2)=1 en retos de Fibonacci)
  - contenido final que no es ZIP (texto, imagen, etc.)
"""
from __future__ import annotations

import argparse
import io
import os
import sys
import zipfile

FIRMAS_ZIP = (b"PK\x03\x04", b"PK\x05\x06")


def es_zip(data: bytes) -> bool:
    return data.startswith(FIRMAS_ZIP)


def recorrer(zf: zipfile.ZipFile, destino: str, nivel: int, max_depth: int,
             visitados: set[bytes]) -> str | None:
    prefijo = f"{nivel:03d}"
    carpeta = os.path.join(destino, prefijo)
    os.makedirs(carpeta, exist_ok=True)

    for info in zf.infolist():
        if info.is_dir():
            continue
        nombre = os.path.basename(info.filename) or "sin_nombre"
        marcador = (info.filename, info.file_size, info.CRC)
        if marcador in visitados:
            # Colisión de nombres típica de secuencias Fibonacci
            nombre = f"{nombre}.dup{len(visitados)}"
        visitados.add(marcador)

        try:
            data = zf.read(info)
        except RuntimeError:
            print(f"[!] nivel {nivel}: '{info.filename}' está cifrado — detener aquí")
            return None

        if es_zip(data):
            print(f"  nivel {nivel:>3}: {info.filename} → ZIP ({len(data)} B)")
            if nivel >= max_depth:
                print("[!] profundidad máxima alcanzada")
                return None
            interno = zipfile.ZipFile(io.BytesIO(data))
            resultado = recorrer(interno, destino, nivel + 1, max_depth, visitados)
            if resultado is not None:
                return resultado
        else:
            ruta = os.path.join(carpeta, nombre)
            with open(ruta, "wb") as fh:
                fh.write(data)
            ratio = sum(1 for b in data if 32 <= b < 127 or b in (9, 10, 13))
            legible = ratio / len(data) if data else 0
            print(f"  nivel {nivel:>3}: {nombre} ({len(data)} B, "
                  f"{legible:.0%} imprimible) → {ruta}")
            if legible > 0.85 and len(data) < 4096:
                print(f"       contenido: {data.decode('utf-8', 'replace').strip()[:200]}")
            return ruta
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Desanidar ZIPs")
    ap.add_argument("archivo")
    ap.add_argument("--out", default="work/capas")
    ap.add_argument("--max-depth", type=int, default=300)
    args = ap.parse_args()

    with open(args.archivo, "rb") as fh:
        data = fh.read()
    if not es_zip(data):
        print("[!] el archivo no es un ZIP")
        return 1

    os.makedirs(args.out, exist_ok=True)
    raiz = zipfile.ZipFile(io.BytesIO(data))
    print(f"raíz: {args.archivo} ({len(raiz.infolist())} entradas)")
    final = recorrer(raiz, args.out, 0, args.max_depth, set())
    print(f"\n[+] contenido final: {final}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
