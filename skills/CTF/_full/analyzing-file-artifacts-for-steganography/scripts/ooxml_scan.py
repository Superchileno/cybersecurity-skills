#!/usr/bin/env python3
"""Escanea un documento OOXML (DOCX/XLSX/PPTX) buscando contenido oculto.

Uso:
    python ooxml_scan.py reto.docx
    python ooxml_scan.py reto.docx --out work/ooxml
    python ooxml_scan.py reto.docx --repair -o work/reparado.docx

Detecta:
  - texto con color blanco, w:vanish, tamaño mínimo
  - partes customXml / docProps / comments / headers / footers
  - blobs Base64 y cadenas hex largas en cualquier XML
  - imágenes y objetos embebidos (los lista para análisis posterior)
  - firma dañada (ofrece reparar los 4 primeros bytes)
"""
from __future__ import annotations

import argparse
import base64
import binascii
import os
import re
import sys
import zipfile

FIRMA_ZIP = b"PK\x03\x04"
PARTES_INTERESANTES = re.compile(
    r"(customXml/|docProps/|comments\.xml|header\d*\.xml|footer\d*\.xml|"
    r"media/|embeddings/|settings\.xml|footnotes\.xml|endnotes\.xml)"
)
RUN_BLANCO = re.compile(
    r"<w:r\b[^>]*>.*?</w:r>", re.S
)
PATRONES_OCULTO = [
    (re.compile(r'w:color\s+w:val="(?:FFFFFF|ffffff|F2F2F2)"'), "color blanco"),
    (re.compile(r"<w:vanish\b"), "texto oculto (vanish)"),
    (re.compile(r'w:sz\s+w:val="(?:[1-8])"'), "tamaño mínimo"),
    (re.compile(r"<w:del\b"), "texto borrado (track changes)"),
    (re.compile(r"<w:instrText\b"), "campo (instrText)"),
]
TEXTO = re.compile(r"<w:t[^>]*>(.*?)</w:t>", re.S)
RE_B64 = re.compile(r"[A-Za-z0-9+/]{24,}={0,2}")
RE_HEX = re.compile(r"\b(?:[0-9a-fA-F]{2}){16,}\b")


def reparar_firma(ruta: str) -> str:
    with open(ruta, "rb") as fh:
        data = fh.read()
    if data[:4] == FIRMA_ZIP:
        return ruta
    print(f"[!] firma inválida: {data[:4].hex(' ')} (se esperaba 50 4b 03 04)")
    reparada = data[:4].replace(data[:4], FIRMA_ZIP, 1) + data[4:]
    destino = os.path.splitext(ruta)[0] + "_reparado.docx"
    with open(destino, "wb") as fh:
        fh.write(reparada)
    print(f"[+] reparado en: {destino}")
    return destino


def extraer_runs_ocultos(xml: str) -> list[str]:
    hallazgos = []
    for m in RUN_BLANCO.finditer(xml):
        bloque = m.group(0)
        for patron, motivo in PATRONES_OCULTO:
            if patron.search(bloque):
                textos = TEXTO.findall(bloque)
                if textos:
                    hallazgos.append(
                        f"{motivo}: {''.join(textos).strip()[:200]}"
                    )
                break
    return hallazgos


def main() -> int:
    ap = argparse.ArgumentParser(description="Escáner OOXML")
    ap.add_argument("documento")
    ap.add_argument("--out", help="extraer el paquete a esta carpeta")
    ap.add_argument("--repair", action="store_true", help="reparar firma dañada")
    args = ap.parse_args()

    ruta = reparar_firma(args.documento) if args.repair else args.documento

    try:
        zf = zipfile.ZipFile(ruta)
    except zipfile.BadZipFile as exc:
        print(f"[!] no es un ZIP válido: {exc}")
        print("    prueba --repair si la firma no es PK\\x03\\x04")
        return 1

    if args.out:
        zf.extractall(args.out)
        print(f"[+] paquete extraído en {args.out}\n")

    nombres = zf.namelist()
    print(f"partes: {len(nombres)}")
    interesantes = [n for n in nombres if PARTES_INTERESANTES.search(n)]
    print("partes de interés:")
    for n in interesantes:
        print(f"  - {n} ({zf.getinfo(n).file_size} B)")

    print("\n--- búsqueda de contenido oculto ---")
    for nombre in nombres:
        if nombre.endswith(".xml") or nombre.endswith(".rels"):
            try:
                xml = zf.read(nombre).decode("utf-8", "replace")
            except KeyError:
                continue
            runs = extraer_runs_ocultos(xml)
            if runs:
                print(f"\n[{nombre}]")
                for r in runs:
                    print(f"  * {r}")

    print("\n--- blobs codificados ---")
    for nombre in nombres:
        if not (nombre.endswith(".xml") or nombre.endswith(".rels")):
            continue
        xml = zf.read(nombre).decode("utf-8", "replace")
        for m in RE_B64.finditer(xml):
            cand = m.group(0)
            try:
                crudo = base64.b64decode(cand + "=" * (-len(cand) % 4))
            except (binascii.Error, ValueError):
                continue
            if crudo[:2] == b"PK" or crudo[:2] == b"\x1f\x8b":
                print(f"  [{nombre}] Base64 → firma {crudo[:4].hex(' ')} "
                      f"({len(crudo)} B): {cand[:40]}…")
        for m in RE_HEX.finditer(xml):
            cand = m.group(0)
            print(f"  [{nombre}] hex {len(cand)//2} B: {cand[:48]}…")

    print("\n--- binarios internos ---")
    for n in nombres:
        if n.startswith(("word/media/", "word/embeddings/", "xl/media/", "ppt/media/")):
            print(f"  - {n} ({zf.getinfo(n).file_size} B) → aplicar pipeline de imágenes")

    return 0


if __name__ == "__main__":
    sys.exit(main())
