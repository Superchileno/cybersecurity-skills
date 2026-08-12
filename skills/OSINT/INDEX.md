# OSINT — Subskills de inteligencia de fuentes abiertas

Área: recon pasivo, búsqueda por username, secretos en código público, footprinting.
Fuente completa: `skills/_src/recon-skills/redteam/*osint*`,
`skills/_src/recon-skills/recon/*secret*`, `skills/_src/hermes-security/sherlock`,
`skills/_src/mukul-anthropic/*`.

## Subskills destiladas

| Subskill | Cuándo usarla | Fuente |
|---|---|---|
| `SKILL-SHERLOCK.md` | Encontrar cuentas de un username en 400+ plataformas | `hermes-security/sherlock/SKILL.md` (oficial) |
| `SKILL-OSINT.md` | Metodología OSINT ofensiva + expansión de sector | `redteam/offensive-osint`, `redteam/osint-methodology` |
| `SKILL-SECRETOS.md` | Caza de secretos/credenciales en repos públicos | `recon/github-secret-hunting`, `recon/hardcoded-credential-hunt` |
| `SKILL-GDORKS.md` | Google dorks / catálogos de dorks | `meta/google-dorks-catalog` |
| `SKILL-SPIDERFOOT.md` | OSINT automatizado multi-módulo (SpiderFoot) | `mukul-anthropic/performing-osint-with-spiderfoot` |
| `SKILL-ACTOR-OSINT.md` | Perfil de actor de amenazas desde OSINT/CTI | `mukul-anthropic/building-threat-actor-profile-from-osint` |

## Enrutado al _src (para detalle)

- GitLab público / source leak: `recon/gitlab-public-recon`, `recon/source-leak-hunt`
- Staging o subdominios olvidados: `recon/staging-subdomain-hunt`
- Email OSINT: `recon/email-security`

## Recuerda (guardrails)

- OSINT pasivo (no deja rastro): ok sobre cualquier dato público.
- Cualquier dato de terceros: redactar PII. Solo para fines autorizados.
- `sherlock`: buscar solo usernames propios o con permiso (ética de la skill).