---
name: redes-vhost
description: 'Cuando el IP responde a un default site (misma web) y el dominio da otro contenido, o hay subdominios no frenados por el servidor. Útil en hosts virtuales de Apache/nginx. Keywords: redes, vhost.'
area: REDES
tags: [redes, vhost]
license: Apache-2.0
---

# SKILL-VHOST.md — Enumeración de virtual hosts

## Cuándo usarla
Cuando el IP responde a un default site (misma web) y el dominio da otro contenido,
o hay subdominios no frenados por el servidor. Útil en hosts virtuales de Apache/nginx.

## Procedimiento resumido
1. Confirmar VHost: `curl -H "Host: noexiste.<domain>" <ip>` vs `Host: <domain>`.
2. Fuzzear Host headers:
   `ffuf -u <IP> -H "Host: FUZZ.<domain>" -w <wordlist> -fc 403,404,500` 
   (también `gobuster vhost -u <ip> -w <subdomains> --append-domain`).
3. Validar respuestas diferenciales (status/body/longitud).
4. Probar también con SNI: `curl --resolve fuzz.<domain>:443:<ip> https://fuzz.<domain>/`.

## Herramientas
`curl`, `ffuf`, `gobuster`, `withSNI` variantes.

## Guardrails
- El fuzzing de vhosts es solicitación de HTTP: solo a hosts en alcance.
- Evidenciar la diferencia de respuesta que demuestra el vhost.