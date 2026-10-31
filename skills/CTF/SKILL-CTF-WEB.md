---
name: ctf-web
description: 'Explotación web de CTF: SQLi (UNION, blind, time-based, error-based y
  bypass de WAF), XSS y bypass de CSP, SSTI, SSRF con callbacks externos, XXE,
  deserialización insegura, fallos de JWT/OAuth/SAML, prototype pollution y cadenas
  con CVEs conocidos. Usar cuando el reto entregue una URL, un servicio HTTP o el
  código de una aplicación web.
  Keywords: CTF web, SQLi, blind SQLi, XSS, CSP bypass, SSTI, SSRF, XXE, JWT, OAuth,
  SAML, prototype pollution, deserialization, web3.'
area: CTF
tags: [ctf, web, sqli, xss, ssti, ssrf, jwt, deserialization]
source: _src/ljagiello-ctf-skills/ctf-web
license: MIT
upstream: ljagiello/ctf-skills
---

# SKILL-CTF-WEB.md — Explotación web

Profundidad en `_src/ljagiello-ctf-skills/ctf-web/`.

## Cuándo usarla
El reto da una URL, un servicio HTTP/API, una SPA o el código de la aplicación.

## Procedimiento resumido
1. Recon: rutas, cabeceras, cookies, tecnologías, robots y endpoints ocultos.
2. Preguntas de entrada: ¿dónde se refleja la entrada?, ¿qué se firma?, ¿qué se
   deserializa?, ¿qué se busca en el servidor?
3. Elegir familia: inyección (SQLi/SSTI/XXE), control de acceso (IDOR/BFLA),
   cliente (XSS/CSP/prototype pollution) o sesión (JWT/OAuth/SAML).
4. Confirmar con la variante mínima; recién después automatizar.
5. Con callback disponible, usarlo para cegueras: SSRF, XXE, XSS, OAuth redirect.
6. Si el stack tiene versión conocida, cruzar con CVEs antes de inventar cadenas.

## Enrutado al `_src`
| Técnica | Archivo |
|---|---|
| SQLi completa | `ctf-web/sql-injection.md` |
| Server-side base y avanzado | `ctf-web/server-side*.md` |
| Deserialización | `ctf-web/server-side-deser.md` |
| Ejecución server-side | `ctf-web/server-side-exec*.md` |
| Cliente: XSS, CSP, DOM | `ctf-web/client-side*.md` |
| Auth: JWT, OAuth, SAML | `ctf-web/auth-*.md` |
| Node y prototype pollution | `ctf-web/node-and-prototype.md` |
| CVEs y cadenas | `ctf-web/cves.md` |
| Web3 | `ctf-web/web3.md` |
| Notas de campo | `ctf-web/field-notes.md` |
| Fuzzing asíncrono | `ctf-web/scripts/async_fuzz.py` |

## Herramientas
`curl`, `ffuf`, `sqlmap`, `nuclei`, `jwt_tool`, `ysoserial`, `tplmap`, DevTools.

## Guardrails
- Solo el host y el alcance que declara el reto.
- No lanzar fuerza bruta de credenciales sin confirmar que el reto lo permite.
- Anotar payload, respuesta y versión del servidor como evidencia.
