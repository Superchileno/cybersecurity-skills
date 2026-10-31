#!/usr/bin/env python3
"""Saneador de contenido para publicar skills de CTF.

Elimina flags reales, hosts, IPs, credenciales y nombres de retos, conservando
la técnica. Genera un informe de cada reemplazo.

Uso:
    python tools/sanitize.py --path <archivo-o-carpeta> [--report informe.md]
    python tools/sanitize.py --path <archivo> --check
    python tools/sanitize.py --path <archivo> --dry-run

Las reglas son ordenadas: las frases específicas se aplican antes que las
genéricas para evitar resultados gramaticales extraños.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from collections import Counter

# (patrón, reemplazo, etiqueta)
REGLAS: list[tuple[str, str, str]] = [
    # Frases compuestas primero
    (r"\| `arc-garage` / `discodroid` \| \(revisar antes de procesar\) \| — \|\n", "", "reto"),
    (r"`punto ciego` / `blind-spot`", "`reto-web-2`", "reto"),
    (r"`net` / `wire-grammar`", "`reto-red-1`", "reto"),
    (r"TRAMA CTF 2026 y 8 retos ANCI/HackRocks", "competiciones de CTF reales", "evento"),
    (r"CTF ANCI \(HackRocks, 2026-10-29\)", "competición de CTF (fecha omitida)", "evento"),
    (r"TRAMA CTF 2026", "una competición de CTF", "evento"),
    (r"ANCI/HackRocks", "una competición de CTF", "evento"),
    (r"HackRocks", "la plataforma", "evento"),
    (r"\bANCI\b", "la competición", "evento"),
    (r"el competición", "la competición", "gramatica"),
    # Flags reales -> placeholder genérico
    (r"TRAMACTF\{[^}\n]*\}", "flag{ejemplo}", "flag"),
    (r"TRAMACTF\{", "flag{", "flag"),
    (r"\bTRAMACTF\b", "PREFIJO", "flag"),
    (r"\bTYAMACTF\b", "PREFIJO", "flag"),
    (r"\bWUDPDFWI\b", "PREFIJOX", "flag"),
    # Nombres de retos
    (r"`ooklakappa`", "`reto-web-1`", "reto"),
    (r"\booklakappa\b", "reto-web-1", "reto"),
    (r"`punto ciego`", "`reto-web-2`", "reto"),
    (r"`blind-spot`", "`reto-web-2`", "reto"),
    (r"\bblind-spot\b", "reto-web-2", "reto"),
    (r"`wire-grammar`", "`reto-red-1`", "reto"),
    (r"\bwire-grammar\b", "reto-red-1", "reto"),
    (r"`turno_noche`", "`reto-rev-1`", "reto"),
    (r"\bturno_noche\b", "reto-rev-1", "reto"),
    (r"\bnight_shift\b", "reto-rev-1", "reto"),
    (r"\barc-garage\b", "reto-heap-1", "reto"),
    (r"\bdiscodroid\b", "reto-kernel-1", "reto"),
    (r"\bsigcall\b", "reto-pwn-1", "reto"),
    (r"\bfireburned\b", "reto-web-3", "reto"),
    # Claves y passphrases de ejemplo
    (r"nightgate", "passphrase", "clave"),
    (r"SweetBl00d", "CLAVE", "clave"),
    (r"SweetBlood", "CLAVE", "clave"),
    (r"nodo_trama_2026", "clave_de_ejemplo", "clave"),
    (r"trama_session", "session_id", "clave"),
    (r'"TRAMA"', '"CLAVE"', "clave"),
    (r"`TRAMA`", "`CLAVE`", "clave"),
    (r"\bTRAMA\b", "CLAVE", "clave"),
    (r"\bMRATA\b", "EVALC", "clave"),
    # Hosts, IPs y puertos
    (r"0\.cloud\.chals\.io", "host.ejemplo", "host"),
    (r"[\w.-]*\.chals\.io", "host.ejemplo", "host"),
    (r"challenges2?\.hackrocks\.com", "host.ejemplo", "host"),
    (r"\b(?:\d{1,3}\.){3}\d{1,3}\b", "_ip_segura", "ip"),
    (r"--port 31547", "--port 1337", "puerto"),
    # Shortlinks
    (r"https?://rb\.gy/[A-Za-z0-9]+", "https://rb.gy/xxxx", "shortlink"),
    (r"/(?:anci4a|anci3a|3bj4pt)\b", "/xxxx", "shortlink"),
    # Rutas del proyecto de origen
    (r"ctf/susurro/ChismeAudio\.wav", "reto/audio.wav", "ruta"),
    (r"Coro_Treinta_Voces", "audio_coro", "ruta"),
    (r"ChismeAudio\.wav", "audio.wav", "ruta"),
]


PRIVADAS = ("127.", "10.", "192.168.", "172.16.", "172.17.", "172.18.", "172.19.",
            "172.2", "172.30.", "172.31.", "0.", "255.", "169.254.")


def _ip_segura(m: re.Match) -> str:
    """Solo sustituye IPs públicas; conserva loopback y rangos privados."""
    valor = m.group(0)
    if valor.startswith(PRIVADAS):
        return valor
    return "10.0.0.10"


def compilar() -> list[tuple[re.Pattern, object, str]]:
    salida = []
    for patron, reemplazo, etiqueta in REGLAS:
        fn = _ip_segura if reemplazo == "_ip_segura" else reemplazo
        salida.append((re.compile(patron), fn, etiqueta))
    return salida


def sanear_texto(texto: str, reglas) -> tuple[str, list[tuple[str, str, int]]]:
    cambios: list[tuple[str, str, int]] = []
    for patron, reemplazo, etiqueta in reglas:
        coincidencias = patron.findall(texto)
        if coincidencias:
            texto = patron.sub(reemplazo, texto)
            cambios.append((etiqueta, str(coincidencias[:3]), len(coincidencias)))
    return texto, cambios


def iterar_archivos(ruta: str):
    if os.path.isfile(ruta):
        yield ruta
        return
    for raiz, _, archivos in os.walk(ruta):
        for nombre in archivos:
            yield os.path.join(raiz, nombre)


def main() -> int:
    ap = argparse.ArgumentParser(description="Saneador de contenido CTF")
    ap.add_argument("--path", required=True)
    ap.add_argument("--report")
    ap.add_argument("--check", action="store_true",
                    help="solo detecta, no modifica; falla si hay coincidencias")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    reglas = compilar()
    total = Counter()
    detalle = []
    revisados = 0

    for ruta in iterar_archivos(args.path):
        if not ruta.endswith((".md", ".py", ".sh", ".c", ".txt", ".yaml", ".yml", ".json")):
            continue
        try:
            with open(ruta, "r", encoding="utf-8") as fh:
                texto = fh.read()
        except (OSError, UnicodeDecodeError):
            continue
        revisados += 1
        nuevo, cambios = sanear_texto(texto, reglas)
        if not cambios:
            continue
        for etiqueta, muestra, n in cambios:
            total[etiqueta] += n
        detalle.append((ruta, cambios))
        if not args.check and not args.dry_run and nuevo != texto:
            with open(ruta, "w", encoding="utf-8") as fh:
                fh.write(nuevo)

    print(f"archivos revisados: {revisados}")
    if not detalle:
        print("[+] sin coincidencias")
    else:
        print(f"archivos con cambios: {len(detalle)}")
        for etiqueta, n in total.most_common():
            print(f"  {etiqueta:<10} {n}")
        for ruta, cambios in detalle:
            print(f"\n  {ruta}")
            for etiqueta, muestra, n in cambios:
                print(f"    - {etiqueta}: {n}  ej: {muestra[:90]}")

    if args.report:
        with open(args.report, "w", encoding="utf-8") as fh:
            fh.write("# Informe de saneamiento\n\n")
            fh.write(f"Archivos revisados: {revisados}\n\n")
            fh.write("| Archivo | Etiqueta | Cambios | Muestra |\n|---|---|---|---|\n")
            for ruta, cambios in detalle:
                for etiqueta, muestra, n in cambios:
                    fh.write(f"| `{ruta}` | {etiqueta} | {n} | `{muestra[:80]}` |\n")
        print(f"\ninforme: {args.report}")

    if args.check and detalle:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
