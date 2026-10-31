---
name: web-ssrf
description: 'Aplicaciones/API que aceptan URLs (previews, proxys, descarga de docs, webhooks, import). Keywords: ssrf, web.'
area: WEB
tags: [ssrf, web]
license: Apache-2.0
---

# SKILL-SSRF.md — Server-Side Request Forgery

## Cuándo usarla
Aplicaciones/API que aceptan URLs (previews, proxys, descarga de docs, webhooks, import).

## Procedimiento resumido
1. Identificar sinks: `url=` `uri=` `next=` `image=` `remote=` `download=`.
2. Probar con IPs internas: `http://127.0.0.1`, `http://169.254.169.254` (cloud
   metadata), rangos privados `10.x`, `172.16-31.x`, `192.168.x`.
3. Confirmación sin dañar: `http://<tu-host>/ssrf-probe` (callback propio), o
   puerto interno con respuesta diferenciada (timing / banner).
4. Variantes: DNS rebinding, redirects, `@`, scheme `gopher://`/`file://` (según filtro),
   `http://0.0.0.0`, decimal/hex IP (`2130706433`).
5. Elevación: SSRF→fuga de metadata cloud, acceso a servicios internos (ver
   `redteam/hunt-ssrf`).

## Clasificación
- Acceso a recurso interno/sin autorización → L3; metadata cloud/credenciales → L4.

## Herramientas
`curl`, Burp Collaborator o tu propio listener (`nc -lvnp`), indicadores DNS.

## Guardrails
- Los callbacks para exfil: host propio, nunca servicios públicos de terceros.
- No sondear internos fuera del alcance del engagement.