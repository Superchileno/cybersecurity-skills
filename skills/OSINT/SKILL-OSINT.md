---
name: osint-osint
description: 'Recon pasivo previo a pentest: footprinting del dominio/persona/organización sin tocar endpoints activos. Keywords: osint.'
area: OSINT
tags: [osint]
license: Apache-2.0
---

# SKILL-OSINT.md — Metodología OSINT ofensiva

## Cuándo usarla
Recon pasivo previo a pentest: footprinting del dominio/persona/organización sin
tocar endpoints activos.

## Procedimiento resumido
1. **Identidad del dominio**: whois, DNS (SPF/DKIM/DMARC), ASN, emails técnicos
   (`recon/email-security`).
2. **Expansión de sector**: `redteam/recon-sector-expansion` — subdominios,
   tecnologías, cuentas asociadas (ver SHERLOCK).
3. **Equipos/personas**: identificando emails y roles (solo con permiso).
4. **Fuga accidental**: GitHub secret hunting, repos públicos, paste/telegram,
   source maps (ver SKILL-SECRETOS).
5. **Consolidar**: mapa de activos (infra→persona→credenciales) sin request
   dañino; guardar evidencias en `evidence/`.

## Referencias _src
- `redteam/offensive-osint`, `redteam/osint-methodology`, `meta/sector-recon-methodology`.

## Guardrails
- OSINT pasivo no deja rastro pero puede tocar datos de terceros: redactar PII.
- No hacer Open-Source Intelligence sobre personas fuera de alcance.
- Solo dentro de targets autorizados del engagement.