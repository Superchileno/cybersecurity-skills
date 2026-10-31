---
name: blueteam-velociraptor
description: 'Hunting/forense a escala en toda una flota de endpoints con Velociraptor (recuperación remota). Keywords: blueteam, velociraptor.'
area: BLUETEAM
tags: [blueteam, velociraptor]
source: '_src/mukul-anthropic/fleet-hunting-with-velociraptor/'
license: Apache-2.0
---

# SKILL-VELOCIRAPTOR.md — Fleet hunting con Velociraptor

Fuente: `_src/mukul-anthropic/fleet-hunting-with-velociraptor/`.

## Cuándo usarla
Hunting/forense a escala en toda una flota de endpoints con Velociraptor (recuperación remota).

## Procedimiento resumido
1. Desplegar servidor Velociraptor y clientes (artifacts para Windows/Linux/mac).
2. Usar **artifact collections**: VQL queries (procesos, netconn, services, registry, prefetch).
3. Hunting masivo: `hunt` sobre flota con artifact creado (p.ej. buscar `mimikatz` en commandline).
4. Forense remota: upload de ficheros/evtx y análisis con notebooks/VQL.
5. Investigación: timeline por host, `artifact collector` para preservar evidencia.
6. Automatizar agents en la flota y programar hunts.

## Herramientas
Velociraptor (server+client), VQL.

## Guardrails
- Acceso admin a todos los endpoints: confirmar autorización de la flota y cumplimiento de privacidad laboral.
- Evidencia redactada (PII) en reportes.