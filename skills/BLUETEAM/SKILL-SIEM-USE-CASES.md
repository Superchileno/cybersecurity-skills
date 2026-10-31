---
name: blueteam-siem-use-cases
description: 'Convertir técnicas ATT&CK en casos de uso SIEM concretos (quién ve qué, con qué fuentes). Keywords: blueteam, cases, siem, use.'
area: BLUETEAM
tags: [blueteam, cases, siem, use]
source: '_src/mukul-anthropic/implementing-siem-use-cases-for-detection/'
license: Apache-2.0
---

# SKILL-SIEM-USE-CASES.md — Casos de uso SIEM de detección

Fuente: `_src/mukul-anthropic/implementing-siem-use-cases-for-detection/`.

## Cuándo usarla
Convertir técnicas ATT&CK en casos de uso SIEM concretos (quién ve qué, con qué fuentes).

## Procedimiento resumido
1. Seleccionar técnicas (MITRE) que el negocio prioriza (por riesgo).
2. Por técnica definir:
   - Datos necesarios (log sources, fields), 
   - Query/correlación,
   - Umbrales y periodicidad,
   - Severidad/prioridad,
   - Owner y playbook de triaje.
3. Etapas: FUENTE→SECCIÓN (parse) → CASO DE USO (detección) → ALERTA (correlación) → INVESTIGACIÓN.
4. Documentar detecciones y medir cobertura (% de técnicas con detección).
5. Ajustar rule por feedback de triaje para reducir FP.

## Guardrails
- Casos de uso triados y medidos; no activar alertas sin playbook.