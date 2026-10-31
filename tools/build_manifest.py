#!/usr/bin/env python3
"""Genera manifest.json a partir de las tarjetas y de skills/CTF/_full/.

Uso:
    python tools/build_manifest.py --repo .
    python tools/build_manifest.py --repo . --check   # falla si el manifiesto está desfasado

Cada entrada declara:
  id          nombre único (= frontmatter `name`)
  area        área de la tarjeta
  kind        "full" si existe versión completa en _full/, si no "lite"
  card        ruta de la tarjeta
  full        ruta del árbol completo o null
  supersedes  ids locales que esta skill reemplaza al instalar
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys

AREAS = ["REDTEAM", "REDES", "WEB", "OSINT", "BLUETEAM", "FORENSE",
         "CUMPLIMIENTO", "CTF"]

# Duplicados temáticos respecto de una instalación local amplia.
SUPERSEDES = {
    "blueteam-beacons": ["hunting-for-cobalt-strike-beacons"],
    "blueteam-chainsaw": ["hunting-evtx-with-chainsaw"],
    "blueteam-deteccion-dcsync": ["detecting-dcsync-attack-in-active-directory"],
    "blueteam-golden-ticket": ["detecting-golden-ticket-attacks-in-kerberos-logs"],
    "blueteam-lateral-splunk": ["detecting-lateral-movement-with-splunk"],
    "blueteam-sigma": ["building-detection-rules-with-sigma"],
    "blueteam-velociraptor": ["fleet-hunting-with-velociraptor"],
    "blueteam-wazuh": ["implementing-endpoint-detection-with-wazuh"],
    "cumplimiento-cmmc": ["achieving-cmmc-level-2-compliance"],
    "cumplimiento-gdpr": ["implementing-gdpr-data-protection-controls"],
    "cumplimiento-iso27001": ["implementing-iso-27001-information-security-management"],
    "cumplimiento-nist-csf": ["performing-nist-csf-maturity-assessment"],
    "cumplimiento-nist-rmf": ["executing-nist-rmf-authorization-to-operate"],
    "cumplimiento-pcidss": ["implementing-pci-dss-compliance-controls"],
    "cumplimiento-riesgo-80030": ["conducting-cyber-risk-assessment-with-nist-800-30"],
    "cumplimiento-tpv": ["managing-third-party-vendor-risk"],
    "forense-autopsy": ["analyzing-disk-image-with-autopsy"],
    "forense-foremost": ["performing-file-carving-with-foremost"],
    "forense-ghidra": ["reverse-engineering-malware-with-ghidra"],
    "forense-hayabusa": ["generating-forensic-timelines-with-hayabusa"],
    "forense-hindsight": ["analyzing-browser-forensics-with-hindsight"],
    "forense-kape": ["triaging-windows-with-kape"],
    "forense-plaso": ["building-super-timelines-with-plaso"],
    "forense-volatility": ["conducting-memory-forensics-with-volatility",
                           "analyzing-memory-dumps-with-volatility"],
    "forense-yara": ["performing-threat-hunting-with-yara-rules",
                     "performing-yara-rule-development-for-detection"],
    "forense-zimmerman": ["performing-windows-artifact-analysis-with-eric-zimmerman-tools"],
    "osint-spiderfoot": ["performing-osint-with-spiderfoot"],
    "redes-bgp-hijack": ["exploiting-bgp-hijacking-vulnerabilities"],
    "redes-shodan": ["performing-ip-reputation-analysis-with-shodan"],
    "redes-ssl-tls": ["performing-ssl-tls-security-assessment"],
    "redteam-entra-attack": ["attacking-entra-id-with-roadtools"],
    "web-hpp": ["performing-http-parameter-pollution-attack"],
    "web-prompt-leak": ["testing-for-system-prompt-leakage"],
    "web-thick-client": ["performing-thick-client-application-penetration-test"],
    "web-xml-injection": ["testing-for-xml-injection-vulnerabilities"],
}

RE_FM = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def leer_frontmatter(texto: str) -> dict[str, str]:
    m = RE_FM.match(texto)
    if not m:
        return {}
    datos: dict[str, str] = {}
    for linea in m.group(1).splitlines():
        if ":" in linea and not linea.startswith((" ", "\t")):
            clave, valor = linea.split(":", 1)
            datos[clave.strip()] = valor.strip().strip("'\"")
    return datos


def construir(repo: str) -> dict:
    entradas = []
    for area in AREAS:
        carpeta = os.path.join(repo, "skills", area)
        if not os.path.isdir(carpeta):
            continue
        for nombre in sorted(os.listdir(carpeta)):
            if not (nombre.startswith("SKILL-") and nombre.endswith(".md")):
                continue
            ruta = os.path.join(carpeta, nombre)
            with open(ruta, "r", encoding="utf-8") as fh:
                texto = fh.read()
            fm = leer_frontmatter(texto)
            ident = fm.get("name")
            if not ident:
                print(f"[!] sin frontmatter: {area}/{nombre}", file=sys.stderr)
                continue
            card = f"skills/{area}/{nombre}"
            full = None
            fuente = fm.get("source", "")
            if fuente.startswith("_full/"):
                candidato = f"skills/CTF/{fuente}"
                if os.path.isfile(os.path.join(repo, candidato, "SKILL.md")):
                    full = candidato
            entradas.append({
                "id": ident,
                "area": area,
                "kind": "full" if full else "lite",
                "card": card,
                "full": full,
                "supersedes": SUPERSEDES.get(ident, []),
            })

    ids = [e["id"] for e in entradas]
    duplicados = sorted({i for i in ids if ids.count(i) > 1})
    if duplicados:
        print(f"[!] ids duplicados: {duplicados}", file=sys.stderr)

    return {
        "version": 1,
        "generated": dt.date.today().isoformat(),
        "areas": AREAS,
        "skills": entradas,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Genera manifest.json")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    datos = construir(args.repo)
    ruta = os.path.join(args.repo, "manifest.json")
    nuevo = json.dumps(datos, ensure_ascii=False, indent=2) + "\n"

    if args.check:
        if not os.path.isfile(ruta):
            print("[!] falta manifest.json")
            return 1
        with open(ruta, "r", encoding="utf-8") as fh:
            actual = fh.read()
        if actual != nuevo:
            print("[!] manifest.json desfasado; ejecuta build_manifest.py")
            return 1
        print("[+] manifest.json actualizado")
        return 0

    with open(ruta, "w", encoding="utf-8") as fh:
        fh.write(nuevo)

    full = sum(1 for e in datos["skills"] if e["kind"] == "full")
    print(f"skills: {len(datos['skills'])} (full: {full}, lite: "
          f"{len(datos['skills']) - full})")
    print(f"escrito: {ruta}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
