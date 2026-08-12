# SKILL-C2-REDIRECT.md — Infraestructura de redirección C2

Fuente: `_src/mukul-anthropic/building-c2-redirector-infrastructure/`.

## Cuándo usarla
Construir la infraestructura de redirección entre implant y C2 para resiliencia/anonimato (red team autorizado).

## Procedimiento resumido
1. Diseñar: dominios/vhosts (similares al target si es para doble-ciega), IPs de saltos.
2. Redirector (nginx/haproxy/iptables) → reenvía tráfico **al C2 real**; `--stream / proxy_pass`.
3. Warmup: servidores "sacrificio" (decoy) responden a IP del C2 en nginx; añadir jitter.
4. Evasión: TLS SNI, HTTP/2, HTTPS con cert válido (o Let's Encrypt), User-Agent rewrite; never directo IP→C2 en prod.
5. Mantenimiento: C2 detrás de 0 o doble hop (cascada); balanceo y failover.
6. Rotar dominios/IP si detección; logs centralizados.

## Herramientas
nginx, haproxy, iptables, Let's Encrypt, sistemas de salto.

## Guardrails
- La infra del red team es del usuario/equipo autorizado; no apuntar a targets fuera de alcance.