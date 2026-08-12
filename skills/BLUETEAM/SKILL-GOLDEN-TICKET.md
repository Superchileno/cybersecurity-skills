# SKILL-GOLDEN-TICKET.md — Detección de Golden Ticket en Kerberos

Fuente: `_src/mukul-anthropic/detecting-golden-ticket-attacks-in-kerberos-logs/`.

## Cuándo usarla
Detectar tickets Kerberos forjados (golden/silver ticket) en logs del DC.

## Procedimiento resumido
1. Habilitar audit de Kerberos (4662/4768/4769 + `Audit Kerberos Service Ticket Operations`).
2. Señales clásicas:
   - TGT con **arca/lifetime anormal** (4768 con duration largo — golden defaults 10h suelen pasar; identificar duración fuera de política).
   - **RID > 1000** en TGT de cuentas humanas (4768 con RID alto → forjado).
   - Horas fuera de patrón de la cuenta.
   - PC utilizado para generar (host desconocido en 4768 source).
3. Correlar 4768 (TGT emitido) + 4769 (S4U) con horarios/IP atípicos.
4. Detección de silver ticket: 4769 con cifrado prefijado (16) para cuentas de servicio y sin 4768 previo de esa cuenta.

## Guardrails
- Solo lectura en prod; validar con equipo de IR. Documentar thresholds con baselines.