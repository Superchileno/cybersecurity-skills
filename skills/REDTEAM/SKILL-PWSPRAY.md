# SKILL-PWSPRAY.md — Password spraying

## Cuándo usarla
Login con protección de bloqueo; en lugar de brute-force agresiva, usar un número
reducido de passwords (comunes/epocal) contra muchos usuarios.

## Procedimiento resumido
1. Coleccionar usernames: enum (logins/registro), OSINT, patrones del target.
2. Elegir 1–3 passwords comunes / del sector (ej. temporada + año, corporate + #).
3. Spray a ritmo moderado: 1 password por lote, esperar entre intentos
   (`-i 30`~`-i 60`+s), nunca golpear el mismo usuario varias veces rápido.
4. Verificar resultado con autenticación real y registrar evidencia mínima.
5. Adaptarse a bloqueos: esperar ventanas de lockout, limitar volumen por IP.
   Ver `redteam/password-spray-methodology` para detalle.

## Herramientas
`hydra` (modo spray), scripts propios con curl, Burp intruder, `crackmapexec/netexec`
para login services.

## Clasificación
- Login válido con credencial débil → L3/L4 (acceso). Intento fallido → L1.

## Guardrails
- Solo contra sistemas autorizados; sin sobrecargar cuentas reales.
- No persistir credenciales capturadas (redactar; secrets-vault gitignored).