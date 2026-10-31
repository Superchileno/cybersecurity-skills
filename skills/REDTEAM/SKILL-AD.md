---
name: redteam-ad
description: 'Red interna con AD (dominios Windows) dentro de alcance autorizado. Keywords: ad, redteam.'
area: REDTEAM
tags: [ad, redteam]
license: Apache-2.0
---

# SKILL-AD.md — Pentest de Active Directory

## Cuándo usarla
Red interna con AD (dominios Windows) dentro de alcance autorizado.

## Procedimiento resumido
1. **Enumeración inicial**: `nmap -sV` coordinadores (SMB, LDAP, DNS, Kerberos).
   `enum4linux-ng <host>` (usuarios, shares, política de passwords).
2. **User enumeration**: null session / `netexec smb <host> --users`, RID cycling
   (`lookupsid`).
3. **Interceptación de red**: `responder -I eth0` (LLMNR/NBT-NS poisoning solo si
   autorizado y en alcance) → capturar hashes NTLMv2.
4. **Kerberoasting**: `netexec ldap <dc> -u <u> -p <p> --kerberoasting` (cuentas SPN)
   → crackear con `hashcat`/`john`.
5. **AS-REP roasting**: usuarios sin preauth Kerberos → `GetNPUsers.py`.
6. **Movimiento lateral**: `nxc smb <subred> -u <u> -H <hash> --shares`, PSExec/WinRM
   (`impacket-psexec`, `evil-winrm` si instalado), Kerberos tickets (`pass-the-ticket`).
7. **Dominio/DACLs** (avanzado): bloodhound (pendiente instalar), DCSync (`secretsdump`).

## Clasificación
- Hash capturado (NTLMv2) → L3; credenciales crackeadas/acceso lateral → L4.

## Herramientas Kali (ya instaladas)
`netexec`, `impacket` (`impacket-psexec`, `secretsdump`, `GetNPUsers`), `responder`,
`enum4linux-ng`, `hashcat`, `john`, `nmap`.

## Guardrails
- Responder/poisoning = activo y puede romper servicios: requiere aprobación
  explícita y alcance interno confirmado.
- Ping de cuenta: evitar bloqueos; log de intentos por usuario.