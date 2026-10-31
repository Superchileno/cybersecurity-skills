---
name: cumplimiento-tpv
description: 'Evaluar y gestionar el riesgo de proveedores/terceros (incluidos procesadores de datos y subcontratistas). Keywords: cumplimiento, tpv.'
area: CUMPLIMIENTO
tags: [cumplimiento, tpv]
source: '_src/mukul-anthropic/managing-third-party-vendor-risk/'
license: Apache-2.0
---

# SKILL-TPV.md — Gestión de riesgo de terceros (vendor risk)

Fuente: `_src/mukul-anthropic/managing-third-party-vendor-risk/`.

## Cuándo usarla
Evaluar y gestionar el riesgo de proveedores/terceros (incluidos procesadores de datos y subcontratistas).

## Procedimiento resumido
1. **Inventario de terceros**: categorizar por criticidad y datos a los que acceden.
2. **Due diligence**: cuestionario de seguridad (SIG Lite/CAIQ), revisar SOC 2/ISO certs, referencias.
3. **Evaluación de riesgo**: adaptar la profundidad al impacto (alta criticidad → assessment on-site o de seguridad exhaustivo). Contratos con cláusulas de seguridad (indemnización, NIC o cancellation).
4. **Contratación**: definir SLA/seguridad en el acuerdo; cláusulas de breach notification.
5. **Monitoreo continuo**: alertas de breaches del proveedor, revisión anual, derechos de auditoría.
6. **Offboarding**: revocar accesos y eliminar datos al terminar relación.

## Referencias
- Marcos: ISO 27001 (8.2), NIST SP 800-161 (supply chain), GDPR (procesadores/DPA).

## Guardrails
- Datos de terceros en evaluaciones redactados; no compartir resultados brutos externamente sin NDA.