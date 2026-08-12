# SKILL-SOC2.md — Preparación de auditoría SOC 2 Type 2

Fuente: `_src/mukul-anthropic/performing-soc2-type2-audit-preparation/`.

## Cuándo usarla
Preparar la organización para el examen SOC 2 (Trust Services Criteria, Type 1/2) por un auditor CPA.

## Procedimiento resumido
1. Definir alcance: sistemas (in-scope), reporte Type 2, periodo de observación (ej. ≥ 12 meses).
2. Seleccionar TSC aplicables (Security + CC6/CC7 y proceso).
3. Documentar **controles** en un "control catalog": diseño, operador, evidencia.
   - Ej: CC6.1 (access), CC6.3 (access removal), CC7.3 (monitoring), CC8.1 (SDLC).
4. Mantener evidencia viva: logs, ticket, test de DR, accesos revocados.
5. Coordinar el examen: auditor pide muestra de evidencias; responder con evidencia diseñada ≠ improvisada.
6. Corregir "exceptions" y publicar el reporte (SOC 2) con opinión del auditor.

## Referencias
- AICPA TSC (2017, actualizado), guías de mapeo con ISO.

## Guardrails
- No fabricar evidencia retroactiva: cada control debe operar realmente durante el periodo.