#!/usr/bin/env python3
"""Extrae y valida candidatos a flag en archivos o por stdin.

Uso:
    python verify_flag.py salida.txt
    cat volcado.txt | python verify_flag.py -
    python verify_flag.py --prefix PREFIJO --prefix flag carpeta/
"""
from __future__ import annotations

import argparse
import os
import re
import sys

PATRONES = [
    re.compile(r"[A-Za-z][A-Za-z0-9_]{2,15}\{[^{}\r\n]{1,200}\}"),
]

# Fragmentos que suelen aparecer en señuelos vistos en retos reales
SENUELOS = [
    "esta_no_es_la_flag",
    "ESTA_NO",
    "no_es_la_flag",
    "PRUEBA",
    "ENSAYO",
    "demo",
    "placeholder",
    "informe_de_caja_equivocado",
    "premio_de_prueba_no_valido",
    "deadbeef",
    "cafebabe",
]


def leer(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    if os.path.isdir(path):
        partes = []
        for raiz, _, archivos in os.walk(path):
            for nombre in archivos:
                ruta = os.path.join(raiz, nombre)
                try:
                    with open(ruta, "rb") as fh:
                        partes.append(fh.read().decode("utf-8", "replace"))
                except OSError:
                    pass
        return "\n".join(partes)
    with open(path, "rb") as fh:
        return fh.read().decode("utf-8", "replace")


def clasificar(candidato: str) -> tuple[str, str]:
    prefijo = candidato.split("{", 1)[0]
    cuerpo = candidato.split("{", 1)[1].rstrip("}")
    cuerpo_l = cuerpo.lower()
    for s in SENUELOS:
        sl = s.lower()
        if cuerpo_l == sl or ("_" in sl and sl in cuerpo_l):
            return "SEÑUELO?", s
    if len(cuerpo) < 8:
        return "SOSPECHOSO", "cuerpo muy corto"
    if not re.search(r"[a-z]{3}", cuerpo):
        return "SOSPECHOSO", "sin palabras legibles"
    return "CANDIDATA", prefijo


def main() -> int:
    ap = argparse.ArgumentParser(description="Detecta y clasifica flags")
    ap.add_argument("rutas", nargs="+")
    ap.add_argument("--prefix", action="append", default=[],
                    help="prefijo esperado (puede repetirse)")
    ap.add_argument("--unique", action="store_true", help="listar sin duplicados")
    args = ap.parse_args()

    vistos: dict[str, str] = {}
    for ruta in args.rutas:
        texto = leer(ruta)
        for patron in PATRONES:
            for m in patron.finditer(texto):
                cand = m.group(0)
                if args.prefix and not any(cand.startswith(p + "{") for p in args.prefix):
                    continue
                if args.unique and cand in vistos:
                    continue
                vistos[cand] = clasificar(cand)[0]

    if not vistos:
        print("[i] sin candidatos")
        return 1

    ancho = max(len(c) for c in vistos)
    for cand, clase in sorted(vistos.items(), key=lambda kv: kv[1]):
        etiqueta, motivo = clasificar(cand)
        print(f"{etiqueta:<11} {cand:<{ancho}}  ({motivo})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
