---
name: blueteam-soar-phantom
description: 'Automatizar respuesta (enrichment, bloqueo, ticketing) entre herramientas con Splunk Phantom. Keywords: blueteam, phantom, soar.'
area: BLUETEAM
tags: [blueteam, phantom, soar]
source: '_src/mukul-anthropic/implementing-soar-automation-with-phantom/'
license: Apache-2.0
---

# SKILL-SOAR-PHANTOM.md — Orquestación/SOAR con Phantom

Fuente: `_src/mukul-anthropic/implementing-soar-automation-with-phantom/`.

## Cuándo usarla
Automatizar respuesta (enrichment, bloqueo, ticketing) entre herramientas con Splunk Phantom.

## Procedimiento resumido
1. Diseñar playbook: trigger (evento SIEM) → actions (enrichment, containment, notification).
2. Conectar apps (SIEM, ticketing, EDR, TI) en Phantom apps (`phantom register`).
3. Construir playbook en el builder visual o desde código Python (app `phantom.py`).
4. Variables: artifacts (IOCs), container (caso), JSON path.
5. Probar en debug mode, validar decisiones, desplegar e ir ampliando cobertura.
6. Mantener KPI de reducción de tiempos de respuesta (ver `building-soc-metrics`).

## Guardrails
- Los playbooks pueden ejecutar acciones destructivas: auditar y aprobar los de alta severidad (bloqueos).
- Secrets (tokens de apps) en vault del SOAR, no en texto plano.