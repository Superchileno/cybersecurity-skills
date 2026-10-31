#!/usr/bin/env python3
"""Valida el repositorio: frontmatter, manifiesto, enlaces y contenido prohibido.

Uso:
    python scripts/validate_skills.py --repo .
    python scripts/validate_skills.py --repo . --verbose

Códigos de salida: 0 = todo correcto, 1 = hay errores.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

AREAS = ["REDTEAM", "REDES", "WEB", "OSINT", "BLUETEAM", "FORENSE",
         "CUMPLIMIENTO", "CTF"]
RE_FM = re.compile(r"\A---\n(.*?)\n---\n", re.S)
RE_LINK = re.compile(r"\]\((SKILL-[A-Z0-9-]+\.md)\)")
RE_FLAG_LARGA = re.compile(r"[A-Za-z][A-Za-z0-9_]{2,20}\{([^}\n]{25,})\}")

PROHIBIDO = [
    (re.compile(r"TRAMACTF", re.I), "prefijo de flag real"),
    (re.compile(r"\.chals\.io", re.I), "host de plataforma"),
    (re.compile(r"hackrocks", re.I), "host de plataforma"),
    (re.compile(r"C:\\Users\\", re.I), "ruta de usuario Windows"),
    (re.compile(r"/mnt/c/", re.I), "ruta absoluta WSL"),
    (re.compile(r"/home/[a-z]+/", re.I), "ruta absoluta Linux"),
]


def leer_frontmatter(texto: str) -> dict[str, str]:
    m = RE_FM.match(texto)
    if not m:
        return {}
    datos = {}
    for linea in m.group(1).splitlines():
        if ":" in linea and not linea.startswith((" ", "\t")):
            clave, valor = linea.split(":", 1)
            datos[clave.strip()] = valor.strip().strip("'\"")
    return datos


def main() -> int:
    ap = argparse.ArgumentParser(description="Validador del repositorio")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    errores: list[str] = []
    avisos: list[str] = []

    # 1. manifest
    ruta_manifest = os.path.join(args.repo, "manifest.json")
    if not os.path.isfile(ruta_manifest):
        errores.append("falta manifest.json")
        manifest = {"skills": []}
    else:
        with open(ruta_manifest, "r", encoding="utf-8") as fh:
            manifest = json.load(fh)

    por_id = {s["id"]: s for s in manifest.get("skills", [])}
    vistos: set[str] = set()
    tarjetas = 0

    # 2. tarjetas
    for area in AREAS:
        carpeta = os.path.join(args.repo, "skills", area)
        if not os.path.isdir(carpeta):
            continue
        for nombre in sorted(os.listdir(carpeta)):
            if not (nombre.startswith("SKILL-") and nombre.endswith(".md")):
                continue
            tarjetas += 1
            ruta = os.path.join(carpeta, nombre)
            with open(ruta, "r", encoding="utf-8") as fh:
                texto = fh.read()
            fm = leer_frontmatter(texto)
            etiqueta = f"{area}/{nombre}"

            if not fm:
                errores.append(f"{etiqueta}: sin frontmatter")
                continue
            ident = fm.get("name", "")
            if not ident:
                errores.append(f"{etiqueta}: falta 'name'")
            if ident in vistos:
                errores.append(f"{etiqueta}: id duplicado '{ident}'")
            vistos.add(ident)
            if fm.get("area") != area:
                errores.append(f"{etiqueta}: area '{fm.get('area')}' != '{area}'")
            desc = fm.get("description", "")
            if len(desc) < 20:
                errores.append(f"{etiqueta}: description demasiado corta")
            if len(desc) > 1024:
                errores.append(f"{etiqueta}: description > 1024 caracteres")
            if ident not in por_id:
                avisos.append(f"{etiqueta}: no está en manifest.json")

            # 3. contenido prohibido
            for patron, motivo in PROHIBIDO:
                if patron.search(texto):
                    errores.append(f"{etiqueta}: {motivo}")

    # 4. skills full
    for s in manifest.get("skills", []):
        if s.get("kind") != "full":
            continue
        base = os.path.join(args.repo, s["full"])
        skill_md = os.path.join(base, "SKILL.md")
        if not os.path.isfile(skill_md):
            errores.append(f"{s['id']}: falta {s['full']}/SKILL.md")
            continue
        with open(skill_md, "r", encoding="utf-8") as fh:
            fm = leer_frontmatter(fh.read())
        if not fm.get("name") or not fm.get("description"):
            errores.append(f"{s['id']}: SKILL.md completo sin frontmatter válido")

    # 5. enlaces de los INDEX
    for area in AREAS:
        index = os.path.join(args.repo, "skills", area, "INDEX.md")
        if not os.path.isfile(index):
            avisos.append(f"{area}: falta INDEX.md")
            continue
        with open(index, "r", encoding="utf-8") as fh:
            texto = fh.read()
        for enlace in RE_LINK.findall(texto):
            if not os.path.isfile(os.path.join(args.repo, "skills", area, enlace)):
                errores.append(f"{area}/INDEX.md: enlace roto a {enlace}")

    # 6. flags largas (posibles flags reales)
    for raiz, dirs, archivos in os.walk(os.path.join(args.repo, "skills")):
        dirs[:] = [d for d in dirs if d != "_src"]
        for nombre in archivos:
            if not nombre.endswith((".md", ".py", ".sh")):
                continue
            ruta = os.path.join(raiz, nombre)
            try:
                with open(ruta, "r", encoding="utf-8") as fh:
                    texto = fh.read()
            except (OSError, UnicodeDecodeError):
                continue
            for m in RE_FLAG_LARGA.finditer(texto):
                errores.append(f"{os.path.relpath(ruta, args.repo)}: "
                               f"posible flag real ({len(m.group(1))} chars)")

    # 7. CLI
    cli = os.path.join(args.repo, "skills", "CTF", "bin", "ctf-arsenal")
    if not os.path.isfile(cli):
        errores.append("falta skills/CTF/bin/ctf-arsenal")

    print(f"tarjetas: {tarjetas} | manifest: {len(por_id)} | "
          f"errores: {len(errores)} | avisos: {len(avisos)}")

    if args.verbose or errores:
        for e in errores:
            print(f"  [x] {e}")
    for a in avisos:
        if args.verbose:
            print(f"  [!] {a}")

    if errores:
        print("\nVALIDACIÓN FALLIDA")
        return 1
    print("\nVALIDACIÓN OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
