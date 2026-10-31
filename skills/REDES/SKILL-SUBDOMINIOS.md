---
name: redes-subdominios
description: 'Recon inicial: ampliar la superficie del dominio objetivo (explosión de alcance). Keywords: redes, subdominios.'
area: REDES
tags: [redes, subdominios]
license: Apache-2.0
---

# SKILL-SUBDOMINIOS.md — Enumeración de subdominios

## Cuándo usarla
Recon inicial: ampliar la superficie del dominio objetivo (explosión de alcance).

## Procedimiento resumido
1. **Pasiva** (sin tocar target): 
   - `subfinder -d <domain> -all` 
   - `amass enum -passive -d <domain>` (si instalado)
   - certificate transparency: `crt.sh` (`curl -s "https://crt.sh/?q=%25.domain&output=json" | jq`)
   - dns brute: `gobuster dns -d <domain> -w <subdomains.txt>` (o `dnsx`).
2. **Activa** (dentro de alcance): `ffuf`/gobuster sobre los SOA/NS, wordlists
   (subdomains-top1million).
3. Verificar resolución y servicios: `dnsx -l sub.txt -a -resp` o `dig`.
4. Subdomain takeover check: alias a servicios cloud extintos → `SKILL-orn
   `subdomain-takeover-hunt` en _src (activity goes to `subdomain-takeover-hunt/SKILL.md`).

## Herramientas
`subfinder`, `amass`, `gobuster`, `ffuf`, `dig`, `dnsx`, `jq`.

## Guardrails
- Brute DNS activo genera consultas al resolver: moderar con `-t`.
- Confirmar que los subdominios encontrados están dentro del alcance pre-declarado.