---
name: cumplimiento-pcidss
description: 'Organizaciones que procesan/almacenan/transmiten datos de tarjetas (CDE): cumplir y auditar PCI DSS. Keywords: cumplimiento, pcidss.'
area: CUMPLIMIENTO
tags: [cumplimiento, pcidss]
source: '_src/mukul-anthropic/implementing-pci-dss-compliance-controls/'
license: Apache-2.0
---

# SKILL-PCIDSS.md — Controles de cumplimiento PCI DSS

Fuente: `_src/mukul-anthropic/implementing-pci-dss-compliance-controls/`.

## Cuándo usarla
Organizaciones que procesan/almacenan/transmiten datos de tarjetas (CDE): cumplir y auditar PCI DSS.

## Procedimiento resimido
1. **Scope**: definir el entorno de datos de tarjeta (CDE) y segregarlo de la red (VLAN/segmentación).
2. Aplicar los 12 requisitos (R1–R12) y sub-requisitos:
   - R1 (firewall), R2 (passwords por defecto), R3 (proteger PAN almacenados), R4 (cifrar transmisión), R5 (proteger contra malware), R6 (seguridad de apps), R7 (acceso por necesidad), R8 (identificación y autenticación MFA), R9 (restringir acceso), R10 (logs y monitoreo), R11 (tests de vulnerabilidad y penetración periódicos), R12 (política).
3. Revisión SAQ/ROC según modelo (merchant → SAQ A/A-EP/D/..., service provider → ROC).
4. Pruebas: escaneo ASV trimestral + penetración anual (para R11).
5. Mitigación con compensaciones (WAS/virtual patch 356/6.4.3) y evidencia para QSA.

## Referencias
- PCI DSS 4.x. Fuente oficial del PCI SSC.

## Guardrails
- Tratar PAN como secreto: redactar primeros 6/últimos 4; nunca desplegar tarjetas reales en tests.