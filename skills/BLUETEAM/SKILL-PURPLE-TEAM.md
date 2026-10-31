---
name: blueteam-purple-team
description: 'Ejercicios purple team (validar detección) y emulación de TTPs con Atomic Red Team. Keywords: blueteam, purple, team.'
area: BLUETEAM
tags: [blueteam, purple, team]
license: Apache-2.0
---

# SKILL-PURPLE-TEAM.md — Purple team / emulación adversarial

Fuentes: `_src/mukul-anthropic/performing-purple-team-exercise/`, `performing-threat-emulation-with-atomic-red-team/`.

## Cuándo usarla
Ejercicios purple team (validar detección) y emulación de TTPs con Atomic Red Team.

## Procedimiento resumido
1. Seleccionar técnicas MITRE a ejercitar (prioridad por riesgo/CTI).
2. **Atomic Red Team** (emulación):
   - Instalar: `Invoke-WebRequest -Uri https://raw.githubusercontent.com/redcanaryco/invoke-atomicredteam/master/install-atomicredteam.ps1 | IEX` (en host test autorizado).
   - Ejecutar: `Invoke-AtomicTest <technique -mitre> -GetPrereqs` → `-TestNumbers 1`.
3. **Purple team (validación)**: coordinar red/blue:
   - Blue: activar y afinar detecciones para la técnica.
   - Comparar telemetría: `deploy-detections` vs gap.
4. Registrar cobertura en MITRE ATT&CK navigator (técnicas detectadas no detectadas).
5. Emitir hallazgos y backlog de mejora de detección.

## Guardrails
- Ejecutar SOLO en entorno de laboratorio/host de test autorizado (no en producción).
- Coordinar con operadores; dejar evidencia de cada prueba.