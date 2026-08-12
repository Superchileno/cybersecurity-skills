# SKILL-NIST-RMF.md — NIST RMF (Authorization to Operate)

Fuente: `_src/mukul-anthropic/executing-nist-rmf-authorization-to-operate/`.

## Cuándo usarla
Implementar el NIST Risk Management Framework (SP 800-37) para autorización a operar de sistemas federales / de alta seguridad.

## Procedimiento resumido
1. **Paso 1 – Categorizar** (SP 800-60): impacto confidencialidad/integridad/disponibilidad → nivel (L/M/H).
2. **Paso 2 – Seleccionar** (SP 800-53): controles base + heredados (FedRAMP) → overrides.
3. **Paso 3 – Implementar**: desplegar y documentar controles.
4. **Paso 4 – Evaluar** (SP 800-53A): tests de controles, evidencias, esfuerzos de remediación.
5. **Paso 5 – Autorizar** (ATO): paquete de seguridad (SSP, SAR, plan) revisado por Authorizing Official.
6. **Paso 6 – Monitorizar** (SP 800-137): evaluaciones continuas, POA&M, actualizaciones.

## Referencias
- NIST SP 800-37 Rev 2, SP 800-53 Rev 5, SP 800-60, FedRAMP (para cloud).

## Guardrails
- La evidencia (test de controles) debe ser real; ATO sin evaluación = ficción legal.