# ENV-KALI.md — Reporte del entorno Kali (WSL2)

Generado: 2026-08-12 (sesión de configuración inicial).

## Sistema

| Atributo | Valor |
|---|---|
| Distribución | Kali GNU/Linux Rolling (2025.4) |
| Kernel | 6.18.33.2-microsoft-standard-WSL2 |
| Usuario | lmiranda (sudo NOPASSWD configurado vía /etc/sudoers.d/lmiranda) |
| CPU | 12 vCPU |
| RAM | 15 GiB total (~14 GiB disponibles) |
| Disco | ~1 TB (WSL2, ~953 GB libres) |
| IP eth0 | 172.28.234.86/20 (WSL NAT) |

## Acceso al entorno

- Bridge desde Windows: `wsl -d kali-linux bash -lc "<cmd>"`
- Ver estado: `wsl -l -v`
- Sudo sin password: `sudo -n <cmd>` (configurado).

## Repositorios apt

- Fuente activa: `https://kali.download/kali` kali-rolling (HTTPS; el mirror HTTP
  devolvía 403). Actualizado 2026-08-12.
- Paquetes instalados: 2107.

## Toolset verificado (smoke test 2026-08-12)

| Área | Herramientas |
|---|---|
| Escaneo/recon | nmap 7.99, gobuster, ffuf, nuclei v3.11.0, nikto |
| Web | sqlmap 1.10.7, burpsuite, wpscan |
| Explotación | metasploit-framework (Console 6.5.0-dev, msfdb conectado a postgresql), hydra |
| Credenciales | hashcat, john (/usr/sbin/john) |
| Movimiento lateral | responder, impacket (impacket-psexec), netexec, enum4linux-ng |
| Blue team | suricata 8.0.6, snort, wireshark |
| Wireless | aircrack-ng |
| Metapackage | kali-linux-headless |

## Notas operativas

- `msfconsole db_status`: `Connected to msf. Connection type: postgresql.`
- Suricata instalado como service deshabilitado (bajo demanda).
- Pendiente validar: bloodhound, Zeek, suite forense (volatility), herramientas de
  compliance (ver sublistas P1.5, P2, P3 en KB-CIBERSEGURIDAD.md).