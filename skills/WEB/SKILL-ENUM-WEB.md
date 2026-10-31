---
name: web-enum-web
description: 'Fase 2 del pentest web / recon: descubrir rutas, archivos, tecnología, source maps. Keywords: enum, web.'
area: WEB
tags: [enum, web]
license: Apache-2.0
---

# SKILL-ENUM-WEB.md — Enumeración web

## Cuándo usarla
Fase 2 del pentest web / recon: descubrir rutas, archivos, tecnología, source maps.

## Procedimiento resumido
1. Tecnología/CMS: `whatweb <url>`; `nmap -p80,443 --script http-title,http-headers`.
2. Rutas/directorios: `gobuster dir -u <url> -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x php,html,txt,json`
   o `ffuf -u <url>/FUZZ -w <lista> -mc 200,301,302,401,403`.
3. Vhosts: ver `REDES/SKILL-VHOST.md`.
4. Source maps / JS: `recon/js-secrets-extraction` (`_src/recon-skills/recon/js-secrets-extraction`).
5. Schema/REST: buscar `/swagger`, `/openapi.json`, `/api-docs`.

## Herramientas Kali
`whatweb`, `gobuster`, `ffuf`, `nmap`, `curl`, `jq`.

## Guardrails
- Solo dentro de alcance; respetar rate-limit de AGENTS.md.
- No usar listas muy grandes sin autorización previa (ruido en logs).