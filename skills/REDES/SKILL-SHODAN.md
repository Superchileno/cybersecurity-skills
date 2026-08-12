# SKILL-SHODAN.md — Reputación de IP con Shodan

Fuente: `_src/mukul-anthropic/performing-ip-reputation-analysis-with-shodan/`.

## Cuándo usarla
Enriquecer pasivamente IPs/activos (servicios, historial, exposición) dentro del alcance OSINT/recon.

## Procedimiento resimido
1. Buscar host: `shodan host <IP>` (API/CLI) → servicios, puertos, banners, vulns conocidas.
2. Buscar por topografía: `shodan search "country:ES product:Apache"`. Guardar filtros por tags.
3. Enriquecimiento: comparar históricos, detectar cambios de servicios (config drift).
4. Reputación: feeds (FireHOL, OTX, AlienVault) marcan IPs abusivas.
5. Automatizar con Python `shodan` CLI en pipelines (enrichment + SOAR).

## Herramientas
Shodan API/CLI (`shodan`), Python `shodan` lib. Requiere API key (el usuario debe aportarla).

## Guardrails
- Solo datos públicos/pasivos; usar la IP del scope; no generar requests a servicios externos injustificadamente.