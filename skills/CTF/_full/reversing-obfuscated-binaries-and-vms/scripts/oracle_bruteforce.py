#!/usr/bin/env python3
"""Fuerza bruta por posición usando un oráculo (conteo de instrucciones o salida).

Uso:
    # Oráculo de instrucciones: más ejecuciones = prefijo más correcto
    python oracle_bruteforce.py --binary ./reto-rev-1 --mode insn \
        --breakpoint 0x1410 --alphabet "abcdefghijklmnopqrstuvwxyz0123456789" \
        --length 10

    # Oráculo de salida: puntúa por longitud/coincidencia con un patrón
    python oracle_bruteforce.py --binary ./binario --mode output \
        --alphabet "abcdefghijklmnopqrstuvwxyz" --length 8 \
        --success "flag{"

Requisitos: gdb para --mode insn.
"""
from __future__ import annotations

import argparse
import os
import re
import string
import subprocess
import sys
import tempfile

PLANTILLA_GDB = """\
set pagination off
set confirm off
python
import gdb
contador = 0
class Contador(gdb.Breakpoint):
    def stop(self):
        global contador
        contador += 1
        return False
Contador("*{bp}")
def al_salir(event):
    print("COUNT=%d" % contador)
gdb.events.exited.connect(al_salir)
end
run < {entrada}
quit
"""


def contar_instrucciones(binario: str, bp: str, datos: bytes) -> int:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".in") as fh:
        fh.write(datos)
        ruta_in = fh.name
    script = PLANTILLA_GDB.format(bp=bp, entrada=ruta_in)
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".gdb") as fh:
        fh.write(script)
        ruta_gdb = fh.name
    try:
        res = subprocess.run(
            ["gdb", "-q", "-batch", "-x", ruta_gdb, binario],
            capture_output=True, text=True, timeout=30,
        )
    finally:
        os.unlink(ruta_in)
        os.unlink(ruta_gdb)
    m = re.search(r"COUNT=(\d+)", res.stdout)
    return int(m.group(1)) if m else 0


def puntuar_salida(binario: str, datos: bytes, exito: str | None) -> float:
    try:
        res = subprocess.run([binario], input=datos + b"\n",
                             capture_output=True, timeout=5)
    except subprocess.TimeoutExpired:
        return 0.0
    salida = (res.stdout + res.stderr).decode("latin-1")
    score = float(len(salida)) / 100.0
    if exito:
        if exito in salida:
            score += 100
        # prefijo parcial del éxito
        for i in range(len(exito) - 1, 2, -1):
            if exito[:i] in salida:
                score += i
                break
    if "denied" in salida.lower() or "incorrect" in salida.lower():
        score -= 1
    return score


def main() -> int:
    ap = argparse.ArgumentParser(description="Fuerza bruta con oráculo")
    ap.add_argument("--binary", required=True)
    ap.add_argument("--mode", choices=["insn", "output"], default="insn")
    ap.add_argument("--breakpoint", help="dirección del fetch del intérprete (insn)")
    ap.add_argument("--alphabet", default=string.ascii_lowercase + string.digits)
    ap.add_argument("--length", type=int, required=True)
    ap.add_argument("--prefix", default="", help="prefijo ya conocido")
    ap.add_argument("--success", help="texto que indica éxito (modo output)")
    args = ap.parse_args()

    if args.mode == "insn" and not args.breakpoint:
        print("[!] --mode insn requiere --breakpoint")
        return 1

    conocido = args.prefix
    print(f"binario: {args.binary}")
    print(f"alfabeto: {len(args.alphabet)} símbolos, longitud {args.length}")
    print(f"prefijo inicial: {conocido!r}\n")

    for pos in range(len(conocido), args.length):
        mejor_simbolo, mejor_score = None, float("-inf")
        for simbolo in args.alphabet:
            candidato = conocido + simbolo
            relleno = "a" * (args.length - len(candidato))
            entrada = (candidato + relleno).encode()
            if args.mode == "insn":
                score = float(contar_instrucciones(args.binary, args.breakpoint, entrada))
            else:
                score = puntuar_salida(args.binary, entrada, args.success)
            if score > mejor_score:
                mejor_score, mejor_simbolo = score, simbolo
        conocido += mejor_simbolo
        print(f"pos {pos + 1}/{args.length}: '{mejor_simbolo}' "
              f"(score {mejor_score:.2f}) → {conocido!r}")

    print(f"\n[+] candidato: {conocido}")
    print(f"    verifica: printf '{conocido}\\n' | {args.binary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
