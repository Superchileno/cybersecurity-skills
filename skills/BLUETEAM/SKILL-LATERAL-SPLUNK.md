# SKILL-LATERAL-SPLUNK.md — Detección de lateral movement con Splunk

Fuente: `_src/mukul-anthropic/detecting-lateral-movement-with-splunk/`.

## Cuándo usarla
Correlacionar movimiento lateral en entorno Windows con Splunk (endpoint logs).

## Procedimiento resumido
1. Fuentes: Sysmon (Event 3 netconn, 1 process, 7/8/10 image load), Security (4624/4634 Logon Type 3/10).
2. Indicadores de LM:
   - `net.exe use` / `net view` remoto;
   - PsExec/SMB exec (service crear + pipes `\\<IP>\IPC$` + `ADMIN$`);
   - WinRM 5985/5986 (Event 8 PowerShell transport);
   - RDP (4648 logon explicit creds + 4624 Type 10).
3. Correlación Splunk: unir logon source ≠ destino del proceso padre inusual; `tstats` sobre index de endpoint.
4. Anomalías: count de logon Type 3 inusual por cuenta/host; `-ComputerName` en procesos.
5. Alert auditadas por cuenta de servicio.

## Herramientas
Splunk (`tstats`, search), Sysmon config.

## Guardrails
- Reglas en jenkins de soberanía: documentar baselines y reducir FP antes de activar alertas.