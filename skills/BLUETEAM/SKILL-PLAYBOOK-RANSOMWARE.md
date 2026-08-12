# SKILL-PLAYBOOK-RANSOMWARE.md — Playbook ransomware con framework CISA

Fuente: `_src/mukul-anthropic/building-ransomware-playbook-with-cisa-framework/`.

## Cuándo usarla
Construir un playbook de respuesta a ransomware alineado a la guía CISA (publication MS-ISAC 2023/2024).

## Procedimiento resumido
1. Preparar línea base: contactos, priorización crítica (CISA), backups offsite/offline, comunicaciones.
2. Fases del playbook:
   - **Detección/analítica**: identificar cifrado (extensiones, banner), contener.
   - **Contención**: aislar hosts/red (no apagar siempre para preservar evidencia), free sinkhole C2.
   - **Erradicación**: limpiar persistencia, rotar credenciales, reviews AD.
   - **Recuperación**: restaurar desde backup externo, validar integridad.
   - **Post-incidente**: lecciones, actualizar playbook.
3. Añadir consideraciones de pago (no recomendar), negociación, timeline kuria.
4. Tabletop y pruebas anuales (`performing-ransomware-tabletop-exercise`).

## Guardrails
- No recomendar pagar rescate; el playbook es un proceso interno de la organización (autorizado por la entidad).