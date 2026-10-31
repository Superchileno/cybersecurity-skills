---
name: ctf-osint
description: 'OSINT de CTF: geolocalización por imagen y Street View, búsqueda inversa
  de imágenes, metadatos EXIF/GPS, enumeración de usuarios y perfiles (X, Tumblr,
  Bluesky, Telegram, GitHub, Steam), coordenadas MGRS y Plus Codes, DNS
  recon, Shodan, dorks de Google y homoglifos Unicode. Usar cuando la respuesta
  esté en fuentes públicas y haya que localizar, identificar o correlacionar.
  Keywords: CTF OSINT, geolocation, reverse image search, EXIF, username enumeration,
  MGRS, plus codes, Shodan, Google dorks, Telegram, Bluesky.'
area: CTF
tags: [ctf, osint, geolocation, exif, shodan, social-media]
source: _src/ljagiello-ctf-skills/ctf-osint
license: MIT
upstream: ljagiello/ctf-skills
---

# SKILL-CTF-OSINT.md — Inteligencia de fuentes abiertas

Profundidad en `_src/ljagiello-ctf-skills/ctf-osint/`.

## Cuándo usarla
El reto pide un lugar, una persona, un objeto, una cuenta o un dato verificable
en fuentes públicas: foto, video, perfil, coordenada o fragmento de texto.

## Procedimiento resumido
1. Extraer todo lo que ya está en el archivo: EXIF, GPS, comentarios, miniaturas.
2. Separar lo verificable (metadatos) de lo interpretable (contexto visual).
3. Geolocalizar por capas: país → ciudad → calle → punto exacto.
4. Buscar la imagen en reversa y comparar recortes, no la imagen completa.
5. Enumerar usuarios y perfiles por alias; correlacionar fechas y estilo.
6. Confirmar con una segunda fuente independiente antes de responder.

## Enrutado al `_src`
| Tema | Archivo |
|---|---|
| Geolocalización y medios | `ctf-osint/geolocation-and-media.md` |
| Redes sociales | `ctf-osint/social-media.md` |
| Web y DNS | `ctf-osint/web-and-dns.md` |
| Herramientas y MCP | `ctf-osint/tools-mcp.md` |

## Herramientas
`exiftool`, `reverse image search`, Google Lens, `what3words`, MGRS converter,
`theHarvester`, `amass`, `shodan`, `wayback`, `sherlock`.

## Guardrails
- Solo fuentes públicas; nada de acceso a cuentas privadas ni ingeniería social.
- No doxear a personas reales: en CTF se responde con la coordenada o el alias.
- Registrar URL y fecha de consulta; el contenido público cambia.
