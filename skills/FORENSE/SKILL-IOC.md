---
name: forense-ioc
description: 'Dentro de una investigación (oss-forensics) o threat hunting: definir y rastrear Indicators of Compromise con trazabilidad evidenciable. Keywords: forense, ioc.'
area: FORENSE
tags: [forense, ioc]
license: Apache-2.0
---

# SKILL-IOC.md — Extracción, enriquecimiento y trazabilidad de IOCs

## Cuándo usarla
Dentro de una investigación (oss-forensics) o threat hunting: definir y rastrear
Indicators of Compromise con trazabilidad evidenciable.

## Procedimiento
1. **Taxonomía** (de `oss-forensics/references/evidence-types.md`):
   `COMMIT_SHA`, `FILE_PATH`, `API_KEY`, `SECRET`, `IP_ADDRESS`, `DOMAIN`,
   `PACKAGE_NAME`, `ACTOR_USERNAME`, `MALICIOUS_URL`, `OTHER`.
2. **Extracción**: computar de prompts/textos/repos con regex (`execute_code`).
3. **Enriquecimiento pasivo** (sin ejecutar código del repo):
   - Commit SHA → `.patch` del API.
   - Dominio/IP → passive DNS/WHOIS.
   - Paquete (npm/pypi) → reporterías de malware/supply-chain.
   - Actor → perfil, antigüedad, contribuciones.
4. **Trazabilidad**: cada IOC enlazado a IDs de evidencia (`EV-XXXX`) y a eventos
   del timeline; marcado `[VERIFIED]`/`[UNVERIFIED]`.

## Referencias _src
- `oss-forensics/references/evidence-types.md`, `recovery-techniques.md`.

## Guardrails
- Mapa del IOC→evidencia siempre; no "enriquecer" con datos no verificados en >1
  fuente. Redactar valores (últimos 6 chars) en el reporte final.