#!/usr/bin/env python3
"""Localiza candidatos a `main` en un ELF stripped.

Uso:
    python find_main.py ./binario
    python find_main.py ./binario --objdump     # forzar análisis con objdump

Método:
  1. Leer el entry point del ELF.
  2. Desensamblar desde él y buscar la llamada a __libc_start_main.
  3. Reportar el `lea rdi, [rip+X]` inmediatamente anterior como main.
  4. Si hay tabla de saltos en .rodata, reportarla (posible VM).

Requiere pyelftools (opcional) y objdump (o capstone).
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys

try:
    from elftools.elf.elffile import ELFFile
except ImportError:
    ELFFile = None


def secciones(ruta: str) -> dict[str, tuple[int, int, int]]:
    """name -> (addr, offset, size)"""
    if ELFFile is None:
        return {}
    with open(ruta, "rb") as fh:
        elf = ELFFile(fh)
        salida = {}
        for s in elf.iter_sections():
            salida[s.name] = (s["sh_addr"], s["sh_offset"], s["sh_size"])
        return salida


def entry_point(ruta: str) -> int:
    if ELFFile is not None:
        with open(ruta, "rb") as fh:
            return ELFFile(fh).header["e_entry"]
    out = subprocess.run(["readelf", "-hW", ruta], capture_output=True, text=True).stdout
    m = re.search(r"Entry point address:\s+0x([0-9a-f]+)", out)
    return int(m.group(1), 16) if m else 0


def desensamblar(ruta: str, inicio: int, largo: int = 160) -> str:
    if not shutil.which("objdump"):
        return ""
    out = subprocess.run(
        ["objdump", "-d", "--start-address", hex(inicio),
         "--stop-address", hex(inicio + largo), ruta],
        capture_output=True, text=True,
    )
    return out.stdout


def buscar_main(ruta: str, ep: int) -> list[int]:
    asm = desensamblar(ruta, ep)
    if not asm:
        return []
    lineas = asm.splitlines()
    candidatos = []
    for i, linea in enumerate(lineas):
        if "__libc_start_main" in linea:
            # Buscar hacia atrás el lea rdi antes de la llamada
            for j in range(i - 1, max(-1, i - 14), -1):
                m = re.search(r"lea\s+0x([0-9a-f]+)\(%rip\),%rdi", lineas[j])
                if m:
                    # Calcular destino: dirección de la instrucción + largo + disp
                    m2 = re.search(r"^\s*([0-9a-f]+):", lineas[j])
                    if m2:
                        ip = int(m2.group(1), 16)
                        disp = int(m.group(1), 16)
                        # largo típico del lea rdi,[rip+disp] = 7
                        candidatos.append(ip + 7 + disp)
                    break
    return candidatos


def tablas_saltos(ruta: str, secs: dict) -> list[tuple[int, int]]:
    """Busca arrays de punteros consecutivos en .rodata que caigan en .text."""
    if not secs or ".rodata" not in secs or ".text" not in secs:
        return []
    addr_ro, off_ro, size_ro = secs[".rodata"]
    addr_tx, _, size_tx = secs[".text"]
    with open(ruta, "rb") as fh:
        fh.seek(off_ro)
        data = fh.read(min(size_ro, 1 << 20))
    candidatos = []
    i = 0
    while i + 8 <= len(data):
        valor = int.from_bytes(data[i:i + 8], "little")
        if addr_tx <= valor < addr_tx + size_tx:
            n, j = 0, i
            while j + 8 <= len(data):
                v = int.from_bytes(data[j:j + 8], "little")
                if not (addr_tx <= v < addr_tx + size_tx):
                    break
                n += 1
                j += 8
            if n >= 4:
                candidatos.append((addr_ro + i, n))
                i = j
                continue
        i += 8
    return candidatos


def main() -> int:
    ap = argparse.ArgumentParser(description="Localiza main y tablas")
    ap.add_argument("binario")
    args = ap.parse_args()

    ep = entry_point(args.binario)
    print(f"entry point: 0x{ep:x}")

    secs = secciones(args.binario)
    if secs:
        print(f"secciones: {len(secs)}")
        for nombre in (".text", ".rodata", ".data", ".bss"):
            if nombre in secs:
                a, o, s = secs[nombre]
                print(f"  {nombre:<8} addr=0x{a:x} offset=0x{o:x} size=0x{s:x}")

    mains = buscar_main(args.binario, ep)
    if mains:
        for m in mains:
            print(f"[+] main candidato: 0x{m:x}")
        print(f"\n    desensambla: objdump -d --start-address=0x{mains[0]:x} "
              f"--stop-address=0x{mains[0] + 0x300:x} {args.binario}")
    else:
        print("[!] no se encontró __libc_start_main en el prólogo")
        print("    prueba: gdb -q binario -ex 'b _start' -ex run -ex 'x/40i $pc'")

    tablas = tablas_saltos(args.binario, secs)
    if tablas:
        print("\n[+] posibles tablas de saltos (dispatch de VM):")
        for addr, n in tablas:
            print(f"    0x{addr:x}: {n} punteros")
    return 0


if __name__ == "__main__":
    sys.exit(main())
