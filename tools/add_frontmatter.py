#!/usr/bin/env python3
"""Añade frontmatter YAML a las tarjetas SKILL-*.md de cada área.

Uso:
    python tools/add_frontmatter.py --repo . [--dry-run]
    python tools/add_frontmatter.py --repo . --only WEB,REDES

Deriva `name` desde el nombre de archivo y `area` desde la carpeta, toma la
descripción de la sección `## Cuándo usarla` y conserva la fuente si la tarjeta
la declara. Es idempotente: no toca tarjetas que ya tengan frontmatter.
"""
from __future__ import annotations

import argparse
import os
import re
import sys

AREAS = ["REDTEAM", "REDES", "WEB", "OSINT", "BLUETEAM", "FORENSE",
         "CUMPLIMIENTO", "CTF"]

RE_TITULO = re.compile(r"^#\s+(SKILL-[A-Z0-9-]+)\.md\s+—\s+(.+)$", re.M)
RE_CUANDO = re.compile(r"^##\s+Cuándo usarla\s*$\n(.*?)(?=^##\s|\Z)",
                       re.M | re.S)
RE_FUENTE = re.compile(r"^Fuente:\s*`([^`]+)`", re.M)


def yaml_str(texto: str) -> str:
    return "'" + texto.replace("'", "''").strip() + "'"


def primera_frase(texto: str, limite: int = 220) -> str:
    limpio = re.sub(r"\s+", " ", texto).strip()
    limpio = re.sub(r"^[-*]\s*", "", limpio)
    if len(limpio) <= limite:
        return limpio
    corte = limpio[:limite].rsplit(" ", 1)[0]
    return corte.rstrip(",;:") + "."


def construir_frontmatter(area: str, archivo: str, contenido: str) -> str | None:
    slug = archivo[len("SKILL-"):-len(".md")].lower()
    prefijo = area.lower() + "-"
    ident = slug if slug.startswith(prefijo) else prefijo + slug

    m_titulo = RE_TITULO.search(contenido)
    titulo = m_titulo.group(2).strip() if m_titulo else slug

    m_cuando = RE_CUANDO.search(contenido)
    resumen = primera_frase(m_cuando.group(1)) if m_cuando else titulo

    palabras = [p for p in re.split(r"[-_]", slug) if p and p not in
                {"skill", "de", "la", "el", "y"}]
    keywords = ", ".join(sorted(set(palabras + [area.lower()])))
    descripcion = f"{resumen} Keywords: {keywords}."

    m_fuente = RE_FUENTE.search(contenido)
    fuente = m_fuente.group(1) if m_fuente else None

    lineas = [
        "---",
        f"name: {ident}",
        f"description: {yaml_str(descripcion)}",
        f"area: {area}",
        f"tags: [{', '.join(sorted(set(palabras + [area.lower()])))}]",
    ]
    if fuente:
        lineas.append(f"source: {yaml_str(fuente)}")
    lineas += ["license: Apache-2.0", "---", ""]
    return "\n".join(lineas)


def main() -> int:
    ap = argparse.ArgumentParser(description="Añade frontmatter a las tarjetas")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--only", help="áreas separadas por coma")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    areas = ([a.strip().upper() for a in args.only.split(",")]
             if args.only else AREAS)
    agregadas = omitidas = 0

    for area in areas:
        carpeta = os.path.join(args.repo, "skills", area)
        if not os.path.isdir(carpeta):
            continue
        for nombre in sorted(os.listdir(carpeta)):
            if not (nombre.startswith("SKILL-") and nombre.endswith(".md")):
                continue
            ruta = os.path.join(carpeta, nombre)
            with open(ruta, "r", encoding="utf-8") as fh:
                contenido = fh.read()
            if contenido.lstrip().startswith("---"):
                omitidas += 1
                continue
            bloque = construir_frontmatter(area, nombre, contenido)
            if bloque is None:
                continue
            nuevo = bloque + "\n" + contenido
            if args.dry_run:
                print(f"[dry] {area}/{nombre}: {len(nuevo)} B")
            else:
                with open(ruta, "w", encoding="utf-8") as fh:
                    fh.write(nuevo)
            agregadas += 1

    print(f"frontmatter añadido: {agregadas} | ya tenían: {omitidas}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
