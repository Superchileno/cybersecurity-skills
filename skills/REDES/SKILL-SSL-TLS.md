# SKILL-SSL-TLS.md — Evaluación de seguridad SSL/TLS

Fuente: `_src/mukul-anthropic/performing-ssl-tls-security-assessment/`.

## Cuándo usarla
Auditar la configuración TLS del target (protocolos, cifrados, certs, configurione) dentro de alcance.

## Procedimiento resimido
1. Escanear: `testssl.sh <host>` (o `--json-pretty`), check protocolos (TLS1.0/1.1/1.3), cifrados, renegotiation, Heartbleed, BEAST/CRIME/POODLE, ROBOT, ALPACA.
2. Manual: `openssl s_client -connect <host>:443 -tls1_2 -cipher 'aNULL'`.
3. Certificados: validez, chain, dates, SAN, CAA/DANE, key size (2048+), sanctions.
4. HSTS/OCSP must-stapling, HPKP no recomendado.
5. Priorizar: TLS1.2/1.3 mínimo, cipher generoso list (ECDHE-RSA-AES128-GCM...), deshabilitar CBC/RC4/anonymous, forward secrecy.

## Herramientas
`testssl.sh` (Kali), `openssl`, `nmap --script ssl-*`, `sslyze`.

## Guardrails
- Escaneo pasivo de config (no ataque activo) — of principal priority ok. No exfil.