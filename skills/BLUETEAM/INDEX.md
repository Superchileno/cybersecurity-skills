# BLUETEAM — Subskills de defensa

Área: monitoreo, detección, threat hunting, incident response, hardening,
threat intelligence, SIEM/SOAR. Fuente: `_src/mukul-anthropic/*` (15 skills) +
`_src/recon-skills` (solo técnica web defensiva).

## Subskills destiladas

| Subskill | Cuándo usarla | Fuente |
|---|---|---|
| `SKILL-SIGMA.md` | Crear/convertir reglas Sigma (detección SIEM-agnóstica) | `building-detection-rules-with-sigma` |
| `SKILL-HUNTING-ELASTIC.md` | Hunting estructurado sobre Elastic/Kibana | `performing-threat-hunting-with-elastic-siem` |
| `SKILL-BEACONS.md` | Detectar Cobalt Strike beacons (JA3/JARM/Zeek/Suricata) | `hunting-for-cobalt-strike-beacons` |
| `SKILL-CHAINSAW.md` | Hunting de evtx a escala con Chainsaw | `hunting-evtx-with-chainsaw` |
| `SKILL-DETECCION-DCSYNC.md` | Detectar DCSync (4662, replicación AD) | `detecting-dcsync-attack-in-active-directory` |
| `SKILL-LATERAL-SPLUNK.md` | Detectar lateral movement con Splunk | `detecting-lateral-movement-with-splunk` |
| `SKILL-GOLDEN-TICKET.md` | Detectar golden/silver tickets Kerberos | `detecting-golden-ticket-attacks-in-kerberos-logs` |
| `SKILL-LOTL.md` | Detectar LOLBins / living off the land | `detecting-living-off-the-land-attacks` |
| `SKILL-WAZUH.md` | EDR/HIDS con Wazuh | `implementing-endpoint-detection-with-wazuh` |
| `SKILL-SOAR-PHANTOM.md` | Automatizar respuesta con Splunk Phantom | `implementing-soar-automation-with-phantom` |
| `SKILL-PLAYBOOK-RANSOMWARE.md` | Playbook ransomware post framework CISA | `building-ransomware-playbook-with-cisa-framework` |
| `SKILL-PURPLE-TEAM.md` | Ejercicios purple team + Atomic Red Team | `performing-purple-team-exercise`, `performing-threat-emulation-with-atomic-red-team` |
| `SKILL-VELOCIRAPTOR.md` | Fleet hunting / forense remoto masivo | `fleet-hunting-with-velociraptor` |
| `SKILL-SIEM-USE-CASES.md` | Diseñar casos de uso SIEM de detección | `implementing-siem-use-cases-for-detection` |

## Enrutado al _src (detalle)

- Fuente completa de estas 15: `skills/_src/mukul-anthropic/<nombre-original>/`.
- Análisis forense de red/super timelines → `skills/FORENSE/`.
- Reglas Suricata/Snort base (herramientas instaladas): ver `docs/ENV-KALI.md`.

## Recuerda (guardrails)

- Hunting/detección sobre datos reales de producción: solo lectura; PII redactada en reportes.
- Los playbooks SOAR con acciones destructivas requieren aprobación previa.