---
name: osint-actor-osint
description: 'Construir un perfil de un grupo/actor de amenazas a partir de OSINT/CTI (TPPs, infra, IOCs) para contexto defensivo. Keywords: actor, osint.'
area: OSINT
tags: [actor, osint]
source: '_src/mukul-anthropic/building-threat-actor-profile-from-osint/'
license: Apache-2.0
---

# SKILL-ACTOR-OSINT.md — Perfil de actor amenaza desde OSINT

Fuente: `_src/mukul-anthropic/building-threat-actor-profile-from-osint/`.

## Cuándo usarla
Construir un perfil de un grupo/actor de amenazas a partir de OSINT/CTI (TPPs, infra, IOCs) para contexto defensivo.

## Procedimiento resumido
1. Recopilar de fuentes CTI: reports (Mandiant, MITRE), threat feeds, darkweb/paste, VT/GreyNose, MISP.
2. Extraer TTPs del actor (MITRE ATT&CK), infraestructura (registrars, hosting, C2), IOCs (domain, IP, hashes, emails).
3. Correlacionar campañas: `correlating-threat-campaigns`, similitud de IOCs.
4. Construir el perfil: unidad/grupo, motivación, víctimas, tools, ALIAS.
5. Documentar en un report accionable (qué buscar en red/endpoint, qué IOCs).

## Referencias
- MITRE ATT&CK Groups, REMnux/TIPs, MISP/PyMISP.

## Guardrails
- Basar el perfil en fuentes citadas (anti-hallucination: cada afirmación con fuente); no atribuir sin evidencia; PII redactada.