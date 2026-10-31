---
name: blueteam-beacons
description: 'Buscar callbacks de Cobalt Strike en tráfico de red / construir detección del C2. Keywords: beacons, blueteam.'
area: BLUETEAM
tags: [beacons, blueteam]
source: '_src/mukul-anthropic/hunting-for-cobalt-strike-beacons/'
license: Apache-2.0
---

# SKILL-BEACONS.md — Hunting de Cobalt Strike beacons

Fuente: `_src/mukul-anthropic/hunting-for-cobalt-strike-beacons/`.

## Cuándo usarla
Buscar callbacks de Cobalt Strike en tráfico de red / construir detección del C2.

## Procedimiento resumido
1. **Firma TLS**: certificado beacon default (serial `8BB00EE`), JA3/JA3S/JARM fingerprints.
2. **Malleable C2 profiles**: patrón HTTP de los perfiles (URI, headers, postdata).
3. **Análisis de jitter/interval**: beacons periodicidad con jitter (intervalos no exactos).
4. Fuentes: logs Zeek (`ssl.log`, `http.log`), reglas Suricata, análisis PCAP en Python.
5. Validar candidatos por contexto (proceso, usuario, alcance interno).

## Herramientas
Zeek, Suricata, `tshark`, Python (scapy/pyshark).

## Guardrails
- Análisis pasivo; si detectas compromiso real → informar y no tocar host hasta decisión de incidentes.