---
name: redes-ct-logs
description: 'Descubrir subdominios/hosts (CT) pasivamente, detectar phishing/cert abusivos, o monitorear emisión de certs del dominio. Keywords: ct, logs, redes.'
area: REDES
tags: [ct, logs, redes]
source: '_src/mukul-anthropic/analyzing-tls-certificate-transparency-logs/'
license: Apache-2.0
---

# SKILL-CT-LOGS.md — Análisis de Certificate Transparency logs

Fuente: `_src/mukul-anthropic/analyzing-tls-certificate-transparency-logs/`.

## Cuándo usarla
Descubrir subdominios/hosts (CT) pasivamente, detectar phishing/cert abusivos, o monitorear emisión de certs del dominio.

## Procedimiento resumido
1. Buscar certs: `crt.sh` via API (`https://crt.sh/?q=%25.domain&output=json`), `crt.sh` de transparencia, herramienta `ctlog` para streaming.
2. Parsear con `jq` deduir subdominios de SAN/DNS, identidades de emisor.
3. Monitorear nuevas emisiones (alerts) para detectar phishing con tu dominio o cert anómalos.
4. Detección de typosquatting: `analyzing-typosquatting-domains-with-dnstwist` (dominios engañosos con cert).
5. Consolidar en mapa de superficie (complementa subdomain enum).

## Herramientas
`crt.sh`/CT log API, `jq`, `dnstwist`, `ct.search`.

## Guardrails
- Datos pasivos (públicos); en phishing confirmado NO visitar el sitio (o hacerlo con tráfico controlado).