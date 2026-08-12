# SKILL-SHERLOCK.md — OSINT de usernames (sherlock)

Skill oficial: `skills/_src/hermes-security/sherlock/SKILL.md`.
Busca en qué plataformas (400+) existe un username.

## Cuándo usarla
Identificar cuentas de un username, verificar disponibilidad, footprinting de persona.

## Procedimiento
1. Verificar instalación: `sherlock --version` (instalado vía pipx en Kali).
2. Comando por defecto: `sherlock --print-found --no-color "<username>" --timeout 90`.
   - Flags solo si el usuario los pide: `--nsfw`, `--tor` (requiere daemon Tor).
3. Parsear resultados: `[+] https://...` y presentarlos agrupados por plataforma.
4. Resultados guardados en `<username>.txt`.

## Pitfalls
- Sin resultados puede ser correcto (username libre). Probar variantes/speaks.
- Timeouts: `--timeout 120`, limitar con `--site`.
- Falsos positivos: algunos sitios siempre devuelven "found" → cross-check manual.

## Guardrails / ética (de la skill oficial)
- Buscar solo usernames propios o con permiso.
- No para acoso/stalking; respetar ToS de plataformas; considerar privacidad
  antes de compartir resultados.
- En un engagement: solo dentro del sujeto autorizado (PII redactada).