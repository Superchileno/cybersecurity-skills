---
name: blueteam-deteccion-dcsync
description: 'Detectar intentos de DCSync (replicación de credenciales DC vía `DS-Replication-Get-Changes*`) en logs de AD. Keywords: blueteam, dcsync, deteccion.'
area: BLUETEAM
tags: [blueteam, dcsync, deteccion]
source: '_src/mukul-anthropic/detecting-dcsync-attack-in-active-directory/'
license: Apache-2.0
---

# SKILL-DETECCION-DCSYNC.md — Detección de DCSync

Fuente: `_src/mukul-anthropic/detecting-dcsync-attack-in-active-directory/`.

## Cuándo usarla
Detectar intentos de DCSync (replicación de credenciales DC vía `DS-Replication-Get-Changes*`) en logs de AD.

## Procedimiento resumido
1. Habilitar **auditing** de replicación (Audit Directory Service Access / 4662 y 4661).
2. Logs clave: Event ID 4662 con GUID `1131f6ad-9c07-11d1-f79f-00c04fc2dcd2` (Replication) por cuentas no-expectadas.
3. Correlación: 4662 (GetChanges/All) + 4624 logon + origen no-DC.
4. Detección también con negocios:
   - Destinos: cuentas con derechos de replicación (solo DCs).
   - Alertar cuentas de servicio/machine accts pidiendo GetChangesAll.
5. Hunting: buscar `DS-Replication-Get-Changes-All` en 4662 de hosts no-DC.

## Guardrails
- Datos reales: solo lectura; reportar al equipo de IR si hay señal fuerte.