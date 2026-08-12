# SKILL-OSS-FORENSICS.md — Forense de supply-chain en GitHub

Skill oficial: `skills/_src/hermes-security/oss-forensics/SKILL.md`.
Investiga repos open-source por compromiso de supply-chain (maintainer takeover,
dependencia maliciosa, force-push, credenciales borradas).

## Cuándo usarla
Incidentes de repos: commits sospechosos, conflictos de dependencias, force-push,
IOCs en el historial.

## Metodología (7 fases, anti-hallucination)
1. **Inicialización**: dir `investigation_<owner>_<repo>/`, evidence store JSON,
   copia del template forense, `iocs.md`, registrar inicio.
2. **Extracción de IOCs**: commit SHAs, actores, ventanas de tiempo, secretos,
   IPs/dominios del prompt.
3. **Recogida en paralelo** (máx 5 investigadores, cada uno 1 sola fuente):
   - Local git: `git fsck --lost-found`, `reflog`, históricos de `.so/.dll/.exe`.
   - GitHub API: commits, PRs, issues, events, releases (rate limit!). 
   - Wayback CDX: páginas/commits borrados.
   - GH Archive/BigQuery: eventos push/delete/force-push (dry-run primero).
   - Enriquecimiento de IOCs (passive only).
4. **Consolidación**: orden temporal, agrupar por actor/IOC, marcar `[VERIFIED]` (2+
   fuentes) vs `[UNVERIFIED]`.
5. **Hipótesis**: plantillas (maintainer compromise, dependency confusion,
   CI/CD injection, typosquat, credential leak). Etiqueta `[HYPOTHESIS]`.
6. **Validación**: verificador mecánico de que cada EV-XXXX citado existe en el
   store; VALIDATED / INCONCLUSIVE / REJECTED (máx 3 iteraciones).
7. **Informe final**: `investigation-report.md` con veredicto (Compromised/Clean/
   Inconclusive + confianza), timeline, EV registry, IOCs, chain of custody,
   recomendaciones (rotar creds, pin hashes, coordinar disclosure).

## Guardrails
- Toda afirmación con cita `EV-XXXX`. SHA/URL doble-verificación. Nunca ejecutar
  código del repo investigado. Secretos → `[REDACTED]`. Uso ético: nada de doxing.