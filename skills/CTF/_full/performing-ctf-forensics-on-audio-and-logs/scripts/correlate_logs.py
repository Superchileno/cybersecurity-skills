#!/usr/bin/env python3
"""Correlaciona logs proxy + backend y reconstruye un payload fragmentado.

Uso:
    python correlate_logs.py --proxy proxy_trace.csv --backend access.log \
        --join rid --status-field proxy_result --ok OK \
        --order flow,seq --payload p --decode base64,deflate

    # Sólo contar eventos por host en un log CEF
    python correlate_logs.py --cef eventos.log --by host

El script es flexible: detecta el delimitador, acepta CSV o JSON lines y reporta
qué flujos producen texto legible tras la decodificación.
"""
from __future__ import annotations

import argparse
import base64
import csv
import gzip
import io
import json
import os
import re
import sys
import zlib
from collections import Counter, defaultdict


def leer_tabla(ruta: str) -> tuple[list[dict], list[str]]:
    """Lee CSV/TSV/JSON-lines y devuelve filas + columnas."""
    with open(ruta, "r", encoding="utf-8", errors="replace") as fh:
        contenido = fh.read()
    lineas = [l for l in contenido.splitlines() if l.strip()]
    if not lineas:
        return [], []
    if lineas[0].lstrip().startswith("{"):
        filas = [json.loads(l) for l in lineas]
        columnas = sorted({k for f in filas for k in f})
        return filas, columnas

    delimitador = max([",", ";", "\t", "|"],
                      key=lambda d: lineas[0].count(d))
    lector = csv.DictReader(io.StringIO(contenido), delimiter=delimitador)
    filas = [dict(f) for f in lector]
    return filas, list(lector.fieldnames or [])


def parsear_cef(ruta: str) -> list[dict]:
    eventos = []
    with open(ruta, "r", encoding="utf-8", errors="replace") as fh:
        for linea in fh:
            if "CEF:" not in linea:
                continue
            partes = linea.strip().split("|")
            if len(partes) < 8:
                continue
            ext = partes[7]
            campos = dict(re.findall(r"(\w+)=([^\s]+)", ext))
            campos["_name"] = partes[4]
            campos["_severity"] = partes[6]
            eventos.append(campos)
    return eventos


def decodificar(cadena: str) -> bytes:
    """Concatena y decodifica un fragmento de payload (base64url tolerante)."""
    limpio = re.sub(r"[^A-Za-z0-9\-_+/]", "", cadena)
    limpio = limpio.replace("-", "+").replace("_", "/")
    limpio += "=" * (-len(limpio) % 4)
    try:
        return base64.b64decode(limpio, validate=False)
    except Exception:  # noqa: BLE001
        return b""


def inflar(data: bytes) -> bytes | None:
    for fn in (zlib.decompress, gzip.decompress,
               lambda d: zlib.decompress(d, -15)):
        try:
            return fn(data)
        except Exception:  # noqa: BLE001
            continue
    return None


def ratio_texto(data: bytes) -> float:
    if not data:
        return 0.0
    return sum(1 for b in data if 32 <= b < 127 or b in (9, 10, 13)) / len(data)


def cmd_correlacionar(args) -> int:
    tablas = {}
    for nombre, ruta in (("proxy", args.proxy), ("backend", args.backend)):
        if not ruta:
            continue
        filas, cols = leer_tabla(ruta)
        tablas[nombre] = (filas, cols)
        print(f"[i] {nombre}: {len(filas)} filas, columnas: {', '.join(cols)}")

    if len(tablas) < 2:
        print("[!] se necesitan --proxy y --backend")
        return 1

    (proxy, _), (backend, _) = tablas["proxy"], tablas["backend"]
    indice = {str(f.get(args.join, "")).strip(): f for f in backend
              if str(f.get(args.join, "")).strip()}
    print(f"[i] unidas por '{args.join}': {len(indice)} claves en backend")

    por_flujo: dict[str, list[dict]] = defaultdict(list)
    orden = [c.strip() for c in args.order.split(",")]

    for fila in proxy:
        clave = str(fila.get(args.join, "")).strip()
        back = indice.get(clave)
        if back is None:
            continue
        estado = str(back.get(args.status_field, fila.get(args.status_field, "")))
        if args.ok and estado.upper() != args.ok.upper():
            continue
        combinada = {**fila, **{f"backend_{k}": v for k, v in back.items()}}
        flujo = str(combinada.get("flow", combinada.get("flujo", "unico")))
        por_flujo[flujo].append(combinada)

    for flujo, filas in por_flujo.items():
        def clave_orden(f):
            valores = []
            for campo in orden:
                v = f.get(campo, f.get(f"backend_{campo}", 0))
                try:
                    valores.append(int(v))
                except (TypeError, ValueError):
                    valores.append(0)
            return tuple(valores)

        filas.sort(key=clave_orden)
        crudo = "".join(str(f.get(args.payload, "")) for f in filas)
        data = decodificar(crudo)
        texto = inflar(data)
        if texto is None:
            texto = data
        r = ratio_texto(texto)
        marca = " <<<" if r > 0.85 and len(texto) > 8 else ""
        print(f"\n[flujo {flujo}] {len(filas)} filas, "
              f"{len(crudo)} chars b64 → {len(data)} B → {len(texto)} B "
              f"({r:.0%} texto){marca}")
        print("  ", texto.decode("latin-1").replace("\r", "")[:300])
    return 0


def cmd_cef(args) -> int:
    eventos = parsear_cef(args.cef)
    print(f"[i] {len(eventos)} eventos CEF")
    campo = args.by
    conteo = Counter(e.get(campo, "?") for e in eventos)
    for valor, n in conteo.most_common():
        print(f"  {n:>3}  {campo}={valor}")

    # Si hay cs1 + cn1, agrupar y decodificar por nombre de evento
    grupos: dict[str, list[tuple[int, str]]] = defaultdict(list)
    for e in eventos:
        if "cs1" in e and "cn1" in e:
            grupos[e.get("_name", "?")].append(
                (int(e["cn1"]) if e["cn1"].isdigit() else 0, e["cs1"]))
    for nombre, pares in grupos.items():
        pares.sort()
        cadena = "".join(p for _, p in pares)
        try:
            texto = base64.b64decode(cadena + "=" * (-len(cadena) % 4))
            print(f"\n[nombre={nombre}] {len(pares)} fragmentos → "
                  f"{texto.decode('latin-1')!r}")
        except Exception:  # noqa: BLE001
            print(f"\n[nombre={nombre}] fragmentos no decodifican juntos")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Correlación de logs CTF")
    ap.add_argument("--proxy", help="CSV/TSV/JSON-lines del proxy")
    ap.add_argument("--backend", help="log/CSV del backend")
    ap.add_argument("--join", default="rid", help="campo de unión")
    ap.add_argument("--status-field", default="proxy_result")
    ap.add_argument("--ok", default="OK")
    ap.add_argument("--order", default="flow,seq")
    ap.add_argument("--payload", default="p")
    ap.add_argument("--decode", default="base64,deflate",
                    help="informativo: el script intenta base64 + inflado")
    ap.add_argument("--cef", help="log en formato CEF")
    ap.add_argument("--by", default="src", help="campo para contar en CEF")
    args = ap.parse_args()

    if args.cef:
        return cmd_cef(args)
    return cmd_correlacionar(args)


if __name__ == "__main__":
    sys.exit(main())
