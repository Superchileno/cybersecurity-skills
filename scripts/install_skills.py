#!/usr/bin/env python3
"""Instala las skills del repositorio en un directorio de skills de agente.

Uso:
    python scripts/install_skills.py --repo . --dest ~/.agents/skills
    python scripts/install_skills.py --repo . --area CTF
    python scripts/install_skills.py --repo . --only web-sqli,ctf-pwn
    python scripts/install_skills.py --repo . --list
    python scripts/install_skills.py --repo . --dry-run

Reglas:
  - kind "full": copia el árbol completo (SKILL.md, references, scripts, assets).
  - kind "lite": materializa <dest>/<id>/SKILL.md con la tarjeta completa.
  - `supersedes`: avisa si el destino ya tiene una skill equivalente; con
    --prune-superseded la mueve a <dest>/.superseded/.
  - Por defecto instala solo el área CTF para no saturar el selector.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def cargar_manifest(repo: str) -> dict:
    ruta = os.path.join(repo, "manifest.json")
    if not os.path.isfile(ruta):
        sys.exit(f"[!] falta {ruta}; ejecuta tools/build_manifest.py")
    with open(ruta, "r", encoding="utf-8") as fh:
        return json.load(fh)


def main() -> int:
    ap = argparse.ArgumentParser(description="Instalador de skills")
    ap.add_argument("--repo", default=RAIZ)
    ap.add_argument("--dest", default=os.path.expanduser("~/.agents/skills"))
    ap.add_argument("--area", default=None,
                    help="área a instalar; 'all' para todas (por defecto CTF)")
    ap.add_argument("--only", default=None, help="ids separados por coma")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--prune-superseded", action="store_true")
    args = ap.parse_args()

    datos = cargar_manifest(args.repo)
    skills = datos["skills"]

    if args.list:
        for s in skills:
            print(f"{s['area']:<13} {s['kind']:<5} {s['id']}")
        print(f"\ntotal: {len(skills)}")
        return 0

    if args.only:
        ids = {i.strip() for i in args.only.split(",") if i.strip()}
        seleccion = [s for s in skills if s["id"] in ids]
        faltan = ids - {s["id"] for s in seleccion}
        if faltan:
            print(f"[!] ids no encontrados: {sorted(faltan)}", file=sys.stderr)
    elif args.area and args.area.lower() != "all":
        seleccion = [s for s in skills if s["area"].lower() == args.area.lower()]
    else:
        seleccion = [s for s in skills if s["area"] == "CTF"]

    if not seleccion:
        print("[!] la selección está vacía")
        return 1

    destino = os.path.abspath(os.path.expanduser(args.dest))
    print(f"repo  : {args.repo}")
    print(f"destino: {destino}")
    print(f"skills : {len(seleccion)}")

    instaladas = omitidas = 0
    for s in seleccion:
        dst = os.path.join(destino, s["id"])
        if os.path.exists(dst) and not args.force:
            print(f"  [skip] {s['id']} ya existe (usa --force)")
            omitidas += 1
            continue

        if args.dry_run:
            origen = s["full"] if s["kind"] == "full" else s["card"]
            print(f"  [dry] {s['kind']:<5} {origen} -> {dst}")
            instaladas += 1
            continue

        if s["kind"] == "full":
            origen = os.path.join(args.repo, s["full"])
            if not os.path.isdir(origen):
                print(f"  [!] falta {origen}")
                continue
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(origen, dst)
        else:
            origen = os.path.join(args.repo, s["card"])
            with open(origen, "r", encoding="utf-8") as fh:
                contenido = fh.read()
            os.makedirs(dst, exist_ok=True)
            with open(os.path.join(dst, "SKILL.md"), "w", encoding="utf-8") as fh:
                fh.write(contenido)
        print(f"  [+] {s['kind']:<5} {s['id']}")
        instaladas += 1

        for viejo in s.get("supersedes", []):
            antiguo = os.path.join(destino, viejo)
            if not os.path.isdir(antiguo):
                continue
            if args.prune_superseded and not args.dry_run:
                basura = os.path.join(destino, ".superseded")
                os.makedirs(basura, exist_ok=True)
                shutil.move(antiguo, os.path.join(basura, viejo))
                print(f"        superseded movido: {viejo}")
            else:
                print(f"        aviso: coexiste con '{viejo}' (usa "
                      f"--prune-superseded)")

    print(f"\ninstaladas: {instaladas} | omitidas: {omitidas}")
    if args.dry_run:
        print("(dry-run: no se escribió nada)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
