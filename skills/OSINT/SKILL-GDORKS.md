# SKILL-GDORKS.md — Google dorks / OSINT con buscadores

## Cuándo usarla
Recon pasivo: encontrar info expuesta no indexada mal en buscadores (archivos,
logs, credenciales de muestra).

## Procedimiento resumido
1. Foco: `site:` `inurl:` `intitle:` `filetype:` `intext:`.
   Palabras golpe: `site:target.com filetype:pdf`, `site:target.com inurl:admin`,
   `intitle:"index of" site:target.com`, `filetype:env`, `intext:"api_key"`.
2. Data leaks en repos: `inurl:github "company" "password"`.
3. Variaciones por idioma/sectores (catálogo de dorks en `_src/meta/google-dorks-catalog`).
4. Compartir hallazgos como índices (no abrir el archivo si es sensible → anotar
   y pedir paso).

## Referencias _src
- `meta/google-dorks-catalog`, `redteam/osint-methodology`.

## Guardrails
- No auto-exec errors al abrir archivos sospechosos; los archivos que aparezcan
  pueden ser maliciosos → descargar con cuidado o solo anexar URL.
- Fuentes externas (Google a veces indexa de terceros) — verificar pertenencia.