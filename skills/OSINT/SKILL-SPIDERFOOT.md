---
name: osint-spiderfoot
description: 'Recon OSINT automatizado (dominios, IPs, emails, people) en 200+ módulos (pasivo mayormente) — complementa a sherlock. Keywords: osint, spiderfoot.'
area: OSINT
tags: [osint, spiderfoot]
source: '_src/mukul-anthropic/performing-osint-with-spiderfoot/'
license: Apache-2.0
---

# SKILL-SPIDERFOOT.md — OSINT con SpiderFoot

Fuente: `_src/mukul-anthropic/performing-osint-with-spiderfoot/`.

## Cuándo usarla
Recon OSINT automatizado (dominios, IPs, emails, people) en 200+ módulos (pasivo mayormente) — complementa a sherlock.

## Procedimiento resumido
1. Lanzar SpiderFoot (CLI o GUI): `spiderfoot -s <domain>` o definiendo scans con `spiderfoot --moduletlist`.
2. Seleccionar scan: pasivo por defecto (no tocar target); activo solo con módulos específicos requeridos.
3. Recorrer módulos: DNS, subdomain, email addresses, IP, ASN, host IP, social, paste/darkweb, breach (si tiene fuentes).
4. Guardar en DB y exportar report CSV/JSON/GEXF.
5. Correlacionar hallazgos con `SKILL-OSINT`/`SKILL-SUBDOMINIOS`.

## Herramientas
SpiderFoot (pip) — requiere módulos (some activos). En Kali no instalado por defecto.

## Guardrails
- Escaneos activos: solo dentro de alcance; no abrir enlaces maliciosos; PII redactada.