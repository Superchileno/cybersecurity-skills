---
name: cumplimiento-riesgo-80030
description: 'Evaluar el riesgo de un sistema/activo siguiendo la metodología de NIST SP 800-30 Rev 1 (o enfoque cualitativo modificado). Keywords: 80030, cumplimiento, riesgo.'
area: CUMPLIMIENTO
tags: [80030, cumplimiento, riesgo]
source: '_src/mukul-anthropic/conducting-cyber-risk-assessment-with-nist-800-30/'
license: Apache-2.0
---

# SKILL-RIESGO-80030.md — Evaluación de riesgo ciber (NIST SP 800-30)

Fuente: `_src/mukul-anthropic/conducting-cyber-risk-assessment-with-nist-800-30/`.

## Cuándo usarla
Evaluar el riesgo de un sistema/activo siguiendo la metodología de NIST SP 800-30 Rev 1 (o enfoque cualitativo modificado).

## Procedimiento resumido
1. **Preparar**: contexto del sistema, amenazas origen relevantes.
2. **Cualitativo/cuantitativo**:
   - Identificar amenazas (actores+TTPs) → Fuente.
   - Vulnerabilidades (scan/tools, sin explotar).
   - Likelihood y impacto (confidencialidad/integridad/disponibilidad).
   - Riesgo = f(likelihood, impacto).
3. Tratamiento: mitigar, transferir, aceptar, evitar (junto al dueño del activo).
4. Priorizar por severidad; documentar con evidencias y mitigaciones.
5. Reportar al equipo de riesgos y re-evaluar periódicamente.

## Referencias
- NIST SP 800-30 Rev 1 (guía), se puede apoyar en CVSS/EPSS para priorización.

## Guardrails
- El riesgo alto sin evidencia no es un hallazgo: vincular cada riesgo con controles/vulnerabilidades concretas.