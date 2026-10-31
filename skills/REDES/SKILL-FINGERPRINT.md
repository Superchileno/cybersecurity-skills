---
name: redes-fingerprint
description: 'Identificar servicios detrás de TLS, detectar WAF/CDN, o evadir detección basada en fingerprint (JA3/JA4) cuando es parte del plan del engagement autorizado. Keywords: fingerprint, redes.'
area: REDES
tags: [fingerprint, redes]
license: Apache-2.0
---

# SKILL-FINGERPRINT.md — Fingerprinting TLS/HTTP y técnicas de disfraz

## Cuándo usarla
Identificar servicios detrás de TLS, detectar WAF/CDN, o evadir detección basada
en fingerprint (JA3/JA4) cuando es parte del plan del engagement autorizado.

## Procedimiento resimido
1. TLS fingerprint: `tls-fingerprint-impersonation` (referencia `_src`)
   — firmas de clientes oficiales (curl, Go, Python) vs bot custom.
2. HTTP/2 header impersonation (`http2-header-impersonation`): emitir cabeceras
   como un navegador real; ver `curl --http2` y extensiones.
3. Detectar WAF/CDN: `whatweb -a 3`, comparar `Server`/`Via`/`X-Cache`, pruebas con
   payloads benignos; IP real → `SKILL-ORIGEN-IP.md`.
4. Reconocimiento de contenedores: análisis de TTL, headers, errores.

## Referencias _src
- `recon/tls-fingerprint-impersonation`, `recon/http2-header-impersonation`, 
  `recon/stealth-browser-launch`.

## Guardrails
- El impersonation es para tests avanzados autorizados; no para ocultar actividad
  fuera de alcance ni evadir protección de terceros.