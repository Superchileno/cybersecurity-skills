#!/usr/bin/env python3
"""Cruza MFT + USN + espacio no asignado para recuperar archivos borrados.

Uso:
    python mft_dat.py --mft mft.csv --usn usn.csv --raw unalloc.raw \
        --cluster 4096 --magic FBLK --out work/

    # Sólo localizar firmas en el volcado
    python mft_dat.py --raw unalloc.raw --scan-magic FBLK

Salida: tabla de candidatos (nombre, DataRun, offset, firma presente) y extracción
del artefacto cuyo offset coincide exactamente con un DataRun.
"""
from __future__ import annotations

import argparse
import csv
import os
import sys


def leer_csv(ruta: str) -> list[dict]:
    with open(ruta, "r", encoding="utf-8", errors="replace") as fh:
        muestra = fh.read(4096)
        fh.seek(0)
        delimitador = max([",", ";", "\t"], key=lambda d: muestra.count(d))
        return [dict(f) for f in csv.DictReader(fh, delimiter=delimitador)]


def buscar_firmas(data: bytes, magic: bytes) -> list[int]:
    posiciones, ini = [], data.find(magic)
    while ini != -1:
        posiciones.append(ini)
        ini = data.find(magic, ini + 1)
    return posiciones


def main() -> int:
    ap = argparse.ArgumentParser(description="MFT + USN + unalloc")
    ap.add_argument("--mft")
    ap.add_argument("--usn")
    ap.add_argument("--raw")
    ap.add_argument("--cluster", type=int, default=4096)
    ap.add_argument("--magic", default=None, help="firma esperada, p.ej. FBLK")
    ap.add_argument("--scan-magic", default=None)
    ap.add_argument("--out", default="work")
    args = ap.parse_args()

    if args.raw and args.scan_magic:
        with open(args.raw, "rb") as fh:
            data = fh.read()
        posiciones = buscar_firmas(data, args.scan_magic.encode())
        print(f"firmas '{args.scan_magic}' en {args.raw}: {len(posiciones)}")
        for p in posiciones:
            print(f"  offset 0x{p:x} ({p}) → clúster {p // args.cluster}")
        return 0

    if not (args.mft and args.raw):
        print("[!] se requiere --mft y --raw (o --raw con --scan-magic)")
        return 1

    filas = leer_csv(args.mft)
    print(f"MFT: {len(filas)} entradas, columnas: {', '.join(filas[0].keys())}")

    with open(args.raw, "rb") as fh:
        raw = fh.read()
    print(f"raw: {len(raw)} B ({len(raw)//args.cluster} clústeres de "
          f"{args.cluster} B)")

    if args.usn:
        usn = leer_csv(args.usn)
        print(f"USN: {len(usn)} eventos")
        for e in usn:
            print("  ", " | ".join(f"{k}={v}" for k, v in e.items()))

    print(f"\n{'nombre':<28} {'borrado':<8} {'DataRun':>8} {'offset':>12} "
          f"{'firma':<8} {'JSON'}")
    candidatos = []
    for fila in filas:
        nombre = next((v for k, v in fila.items()
                       if k.lower() in ("nombre", "name", "filename")), "?")
        borrado = next((v for k, v in fila.items()
                        if k.lower() in ("borrado", "deleted")), "?")
        datarun = next((v for k, v in fila.items()
                        if k.lower() in ("datarun", "cluster", "clúster")), None)
        if datarun is None:
            continue
        try:
            offset = int(str(datarun)) * args.cluster
        except ValueError:
            continue
        firma = "-"
        tiene_json = ""
        if args.magic and raw[offset:offset + len(args.magic)] == args.magic.encode():
            firma = args.magic
            # Intentar leer el JSON de cabecera si el formato es magic+ver+len+json
            try:
                largo = int.from_bytes(raw[offset + 8:offset + 12], "little")
                if 0 < largo < 4096:
                    texto = raw[offset + 12:offset + 12 + largo].decode(
                        "utf-8", "replace")
                    tiene_json = texto[:80]
            except Exception:  # noqa: BLE001
                pass
            candidatos.append((nombre, offset))
        print(f"{nombre:<28} {str(borrado):<8} {str(datarun):>8} "
              f"0x{offset:08x} {firma:<8} {tiene_json}")

    if candidatos:
        os.makedirs(args.out, exist_ok=True)
        print(f"\n[+] {len(candidatos)} artefacto(s) válido(s):")
        for nombre, offset in candidatos:
            destino = os.path.join(args.out, f"recuperado_{offset:x}.bin")
            with open(destino, "wb") as fh:
                fh.write(raw[offset:offset + args.cluster])
            print(f"  {nombre} → {destino}")
        print("\n[i] el artefacto real es el que tiene firma Y cronología "
              "create→overwrite→delete en el USN")
    return 0


if __name__ == "__main__":
    sys.exit(main())
