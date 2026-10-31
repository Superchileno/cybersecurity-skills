---
name: blueteam-chainsaw
description: 'Hunting/forense rápido de eventos Windows (evtx) a escala, sin SIEM, con reglas Sigma embebidas. Keywords: blueteam, chainsaw.'
area: BLUETEAM
tags: [blueteam, chainsaw]
source: '_src/mukul-anthropic/hunting-evtx-with-chainsaw/'
license: Apache-2.0
---

# SKILL-CHAINSAW.md — Hunting de evtx con Chainsaw

Fuente: `_src/mukul-anthropic/hunting-evtx-with-chainsaw/`.

## Cuándo usarla
Hunting/forense rápido de eventos Windows (evtx) a escala, sin SIEM, con reglas Sigma embebidas.

## Procedimiento resumido
1. Instalar Chainsaw (release binary).
2. Barrer logs: `chainsaw hunt --mapping mapping.json -r <dir_evtx>` (reglas Sigma incluidas).
3. Búsqueda por palabras: `chainsaw search <term>` (ej. `mimikatz`, `CertUtil`, `powershell -enc`).
4. Ver resultado el .evtx original: `chainsaw dump`.
5. Exportar hallazgos (JSON/CSV) y correlacionar con otras fuentes.

## Herramientas
`chainsaw` (descargar release de GitHub), reglas Sigma pack.

## Guardrails
- Copia los evtx a triage (no tocar los originales de producción).
- Redactar PII en reportes.