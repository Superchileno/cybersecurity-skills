# SKILL-VOLATILITY.md — Análisis de memoria con Volatility 2/3

Fuentes: `_src/mukul-anthropic/analyzing-memory-dumps-with-volatility/`, `performing-memory-forensics-with-volatility3/`.

## Cuándo usarla
Análisis forense de dumps de memoria RAM (compromiso, malware en memoria).

## Procedimiento resumido
1. Ver imagen: `imageinfo` (Vol2) / `windows.info` (Vol3) → perfil.
2. Procesos: `pslist`/`psscan`/`pstree`; detectar procesos ocultos (psscan vs pslist).
3. Red: `netscan` (sockets/conexiones), `connscan`.
4. Malware: `malfind` (memoria inyectada), `hollowfind`, `dlldlist/api`.
5. Credenciales: `hashdump`, `lsadump`, `cachedump` (redactar).
6. Temporales: `timeliner`, `evtlogs`, `cmdline`, `handles`.
7. Vol3: plugins `windows.malfind`, `windows.pslist`, `linux.*`.

## Herramientas
`volatility` (Vol2) / `volatility3` (pip), dump adquirido con `dd`/`lime` (Linux) o `memdump`.

## Guardrails
- Solo sobre dumps autorizados (propios o engagement); redactar credenciales obtenidas (últimos 6 chars).