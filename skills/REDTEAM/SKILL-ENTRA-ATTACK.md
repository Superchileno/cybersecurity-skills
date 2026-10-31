---
name: redteam-entra-attack
description: 'Post-explotación / pentest de tenants Entra ID (Microsoft Entra) autorizados: abusar de condiciones, tokens, aplicaciones, consenso. Keywords: attack, entra, redteam.'
area: REDTEAM
tags: [attack, entra, redteam]
license: Apache-2.0
---

# SKILL-ENTRA-ATTACK.md — Ataque a Entra ID (M365) con roadtools/GraphRunner

Fuentes: `_src/mukul-anthropic/attacking-entra-id-with-roadtools/`, `post-exploiting-microsoft-graph-with-graphrunner/`.

## Cuándo usarla
Post-explotación / pentest de tenants Entra ID (Microsoft Entra) autorizados: abusar de condiciones, tokens, aplicaciones, consenso.

## Procedimiento resumido
1. **Enumeración**: `roadtx`/`roadrecon` (roadtools): `roadrecon auth -u <u@tenant> -p ap...` → recolectar datos en BD local (`roadrecon gatherapi`, `report`).
2. Indicadores de riesgo: apps con alto privilegio, consenso excesivo, service principals.
3. Atacar:
   - **Device code phishing** (`attacking-oauth-with-device-code-phishing`): abusar flujos de device code → session token.
   - Consenso de aplicación maliciosa (tenant-wide admin consent) → poder Graph.
   - Refrescos token themes / federación SAML (token smuggling).
4. **Post-explotación Graph**: `GraphRunner` (post-exploit) → enumerar apps, mail, drive, users; abuse de `application.ReadWrite` para crear service principal con `GlobalAdmin` (peligro), DCSync no aplica (cloud).
5. Mover lateral a apps cloud; documentar.

## Herramientas
`roadrecon`/`roadtx`, `GraphRunner`, `AzureAD`/`graph` PowerShell.

## Guardrails
- Solo tenant autorizado; no modificar config del tenant (risk); evidencia con logs y screenshots, no dejando backdoors.