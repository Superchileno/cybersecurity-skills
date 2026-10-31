---
name: redes-puertos
description: 'Fase de enum de hosts: mapear puertos/servicios y versiones del target. Keywords: puertos, redes.'
area: REDES
tags: [puertos, redes]
license: Apache-2.0
---

# SKILL-PUERTOS.md — Escaneo de puertos y servicios

## Cuándo usarla
Fase de enum de hosts: mapear puertos/servicios y versiones del target.

## Procedimiento resumido
1. **Triage amplio (rápido)**: `nmap -Pn --top-ports 1000 -T4 <host>` (o `-p-` si
   el alcance y presupuesto de tiempo lo permite; UTC).
2. **Servicios y versiones**: `nmap -sV -sC -Pn -p <puertos> <host>` sobre los
   puertos abiertos detectados (NSE default).
3. **Escala**: para rangos grandes usar `rustscan`/`masscan`+`-oG` y luego nmap
   fino (`port-mass-scan`, `port-service-discovery` en _src).
4. Clasificar servicios + posibles CVEs (NSE vuln scripts SOLO si autorizado y con
   cuidado: pueden ser intrusivos).
5. Guardar outputs en `evidence/` (`-oA <nombre>`).

## Herramientas
`nmap`, `rustscan`, `masscan`, `nc`.

## Guardrails
- Escaneos grandes producen ruido: respetar alcance y rate (AGENTS.md).
- Scripts `--script vuln` son activos y pueden impactar: aprobación previa.
- No escanear hosts fuera de alcance (evitar rango por defecto).