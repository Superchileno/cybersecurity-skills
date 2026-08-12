# SKILL-LOTL.md — Detección de Living off the Land (LOLBins)

Fuente: `_src/mukul-anthropic/detecting-living-off-the-land-attacks/`.

## Cuándo usarla
Detectar abuso de binarios del sistema (LOLBin) para evasión/ejecución de malware.

## Procedimiento resimido
1. Usar el repositorio **LOLBAS** como fuente de técnicas y comandos.
2. Logs: Sysmon Event 1 (process), 7/8/10 (image load), 13/15 (registry), ScriptBlock logging (PowerShell).
3. Patrones clásicos:
   - `rundll32.exe` con `.js/.hta`, `powershell -enc` (codificada),
   - `mshta`, `regsvr32` (scrobj.dll), `certutil -decode`/`-urlcache`,
   - `bitsadmin`/`BITS` transfers, `wmic process call create`, `cmstp`.
4. Correlar con parent process inusuales o cadenas (svchost.exe → cmd.exe).
5. Hunting por hash de scripts en logs PowerShell o scriptblock.

## Herramientas
Sysmon, PowerShell ScriptBlock Logging, LOLBAS project.

## Guardrails
- Los binarios legítimos generan FP: validar contexto antes de escalar.