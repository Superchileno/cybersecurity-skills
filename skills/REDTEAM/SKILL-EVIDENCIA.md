# SKILL-EVIDENCIA.md — Higiene de evidencia

## Cuándo usarla
Toda vez que se captura hallazgo (L3/L4) o se construye el reporte.
Fuente base: `skills/_src/recon-skills/redteam/evidence-hygiene`, `redteam/triage-validation`.

## Reglas
1. **Cada hallazgo L3/L4 requiere**: request completo (método, URL, headers, body),
   response (status, headers, extracto relevante), reproducer `curl`, e impacto.
2. **Redacción**: credenciales/tokens → solo últimos 6 chars en chat; valor completo
   a `findings/secrets-vault.md` (gitignored). PII de terceros → redactar.
3. **Reproducible**: el curl/ofensor debe poderse re-ejecutar tal cual.
4. **Triage antes de reportar**: validar que el hallazgo no es falso positivo
   (`redteam/triage-validation`) — agotar bypass set antes de descartar.
5. **Organización**: `engagements/<nombre>/evidence/`, `findings/`, `reports/`.

## Herramientas
`curl` (reproducer), Burp (guard request/response), scripts del pack (evidencia).

## Guardrails
- Nunca incluir secretos vivos en el reporte final.