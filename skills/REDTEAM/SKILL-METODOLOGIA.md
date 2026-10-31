---
name: redteam-metodologia
description: 'Antes de planear cualquier engagement ofensivo (planning/framework). Keywords: metodologia, redteam.'
area: REDTEAM
tags: [metodologia, redteam]
license: Apache-2.0
---

# SKILL-METODOLOGIA.md — Mindset y metodología ofensiva

## Cuándo usarla
Antes de planear cualquier engagement ofensivo (planning/framework).

## Principios
1. **Autorización y alcance primero** (`AGENTS.md`): target, propiedad/autorización
   escrita, ventana de tiempo, métodos permitidos.
2. **Enfoque goal-oriented**: objetivo de negocio (datos, acceso, credenciales) y
   no solo "escanear todo".
3. **Topología de esfuerzo**: reconocimiento amplio → focos de alto valor →
   profundidad (no pasearse).
4. **Expansión de sector**: solo tras agotar señal del objetivo; nunca pivotar
   sin aprobación explícita (`meta/sector-recon-methodology`, `redteam/recon-sector-expansion`).
5. **Mínima intrusión**: en producción, usar payloads y técnicas que no degraden
   el servicio.

## Referencias _src
- `redteam/redteam-mindset`, `redteam/bb-methodology`, `redteam/recon-sector`,
  `meta/recon-playbook`, `meta/pentest-playbook`.

## Guardrails
- Reportar con lenguaje preciso: "no se encontraron issues explotables en alcance X".
- Documentar metodología utilizada en el reporte.