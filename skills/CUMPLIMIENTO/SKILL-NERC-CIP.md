---
name: cumplimiento-nerc-cip
description: 'Empresas del sector eléctrico (BES: Bulk Electric System) que deben cumplir los estándares NERC CIP. Keywords: cip, cumplimiento, nerc.'
area: CUMPLIMIENTO
tags: [cip, cumplimiento, nerc]
source: '_src/mukul-anthropic/implementing-nerc-cip-compliance-controls/'
license: Apache-2.0
---

# SKILL-NERC-CIP.md — Cumplimiento NERC CIP (infraestructura crítica)

Fuente: `_src/mukul-anthropic/implementing-nerc-cip-compliance-controls/`.

## Cuándo usarla
Empresas del sector eléctrico (BES: Bulk Electric System) que deben cumplir los estándares NERC CIP.

## Procedimiento resumido
1. Identificar activos BES (azority: 由 BES Cyber Systems/BCS según modelos de certificación).
2. Aplicar los estándares CIP:

   | CIP estándar | Tema |
   |---|---|
   | CIP-002 | Clasificación de ciber-sistemas (High/Medium/Low impact) |
   | CIP-003 | Controles de seguridad y gestión |
   | CIP-004 | Personal y training (PRA) |
   | CIP-005 | Perímetro electrónico (ESP) |
   | CIP-006 | Seguridad física |
   | CIP-007 | Gestión de sistemas (parches, malware, monitoreo) |
   | CIP-008 | Incident response y recuperación |
   | CIP-009, 010, 012 | Backup, config change, transients |
   | CIP-014 | Seguridad física de subestaciones |

3. Documentar evidencia (políticas, configs, logs, records de training) para auditoría NERC.
4. Planeación de parches CIP-007 (ciclos), protección física.

## Referencias
- NERC Reliability Standards CIP-002..CIP-014.

## Guardrails
- Entorno OT/ICS: cambios solo con ventanas de aprobación; evidencia de que los controles CIERRA realmente operan.