# SKILL-SECRETOS.md — Caza de secretos en código público

## Cuándo usarla
Buscar credenciales/API keys/tokens expuestos en repos públicos, CI/CD o artefactos
del target (verificación de exposición accidental vs leak intencional).

## Procedimiento resumido
1. **GitHub**: buscar secretos por termás y tokens de la org del target:
   `github-secret-hunting` (referencia _src) — queries de GitHub search,
   grep para `api_key`, `password=`, `AKIA`, `ghp_`, `.env`, etc.
2. **Repo scanning local** (si se accede al repo): `git log -p`, buscar en
   history secrets antiguos (toxic commit), `trufflehog`.
3. **Public artifacts**: npm/pypi packages con tokens embebidos (supply chain),
   Docker Hub, Source maps (`js-secrets-extraction`).
4. Validar el secreto mínimo (no usarlo; solo confirmar exposición): revisar si
   el provider confirma scope (matching metadata origen).

## Herramientas
`trufflehog`, `gitleaks`, `jq`, GitHub search (sin tokens).

## Guardrails
- NUNCA test de validez con el token capturado (puede romper cuenta); no
  persistir/desplegar el secreto. Redactar a últimos 6 chars.
- Solo sobre repos del target o con permiso (evitar investigar terceros).