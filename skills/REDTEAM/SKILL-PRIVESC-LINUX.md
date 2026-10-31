---
name: redteam-privesc-linux
description: 'A partir de una shell de usuario con poca confianza en sistema Linux (dentro de alcance pentest autorizado), subir a root. Keywords: linux, privesc, redteam.'
area: REDTEAM
tags: [linux, privesc, redteam]
source: '_src/mukul-anthropic/performing-privilege-escalation-on-linux/'
license: Apache-2.0
---

# SKILL-PRIVESC-LINUX.md — Escalada de privilegios en Linux

Fuente: `_src/mukul-anthropic/performing-privilege-escalation-on-linux/`.

## Cuándo usarla
A partir de una shell de usuario con poca confianza en sistema Linux (dentro de alcance pentest autorizado), subir a root.

## Procedimiento resumido
1. **Enumeración automática**: `linpeas.sh` (curl a github desde el host), `LinEnum.sh`, `linux-exploit-suggester`.
2. Manual:
   - SUID/SGID: `find / -perm -4000 2>/dev/null` → binarios explotables (`gtfobins`).
   - Crontabs/jobs del root; `capabilities` (`getcap -r /`).
   - Sudo -l (binarios con NOPASSWD → sudo abuse); sudo -e.
   - Cron/path hijack; configs con credenciales (`.bash_history`, configs web).
   - Kernel exploits (obsoletos): `uname -r` + search (CVE). Usados sin destructividad.
3. Confirmar escalada con comando no destructivo (`id`), capturar evidencia.

## Referencias
- GTFOBins (gtfobins.github.io): binarios abusables.

## Guardrails
- Exploits de kernel pueden dejar el sistema inestable: preferir captura local; documentar con `id`, no con daño.