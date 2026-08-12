# KB-CIBERSEGURIDAD.md — Base de conocimientos inicial

Fuentes analizadas: ecosistema Hermes Agent (hermes-ai.net/skills), skill oficial
`security/web-pentest` (metodología Shannon), pack comunitario `recon-skills`,
HermesAtlas (817 skills, 29 dominios, 6 frameworks). Ver `KB-SKILLS.md`.

## Nivel 1 — Lista principal (4 pilares)

1. **Pentesting (Offensive)** — recon → escaneo → explotación → post-explotación
   → reporting. Con guardrails de autorización del AGENTS.md.
2. **Blue Team / Defensa** — detección, monitoreo, threat hunting, incident
   response, hardening, forense, threat intel.
3. **Cumplimiento / Compliance** — marcos normativos, gestión de riesgos,
   controles, auditoría, evidencia.
4. **Fundamentos y Ops** — operación Kali-WSL, scripting, documentación, reportes,
   metodología de trabajo del agente.

## Nivel 2 — Sublistas de profundización

### P1. Pentesting (Offensive)

- **P1.1 Recon / OSINT** — pasivo (Google dorks, Shodan/Censys, search engine
  footprinting, whois/DNS, sherlock para usernames) → activo (subdomain enum,
  vhost discovery, GitHub secret hunting). Tarjetas en `skills/OSINT/` y `skills/REDES/`.
- **P1.2 Enumeración** — nmap (topología, versiones, scripts NSE), ffuf/gobuster
  (directorios, vhosts, fuzz), wfuzz, técnicas de fuzzing.
- **P1.3 Web (OWASP Top 10)** — XSS (reflejado/almacenado/DOM), SQLi, SSRF, RCE,
  IDOR/auth flaws, file upload, CSRF, deserialización, misconfig TLS/headers.
- **P1.4 Infraestructura y servicios** — Metasploit, Hydra (auth brute), servicio
  banner/version exploits, creds dumping local.
- **P1.5 Active Directory / red interna** — enumeration (enum4linux-ng, netexec),
  responder/LLMNR, kerberoasting, AS-REP roasting, movimiento lateral, bloodhound.
- **P1.6 Wireless** — aircrack-ng suite, WPA/WPA2 cracking, wifite (alcance aprobado).
- **P1.7 Explotación proof-based** — verificación L1→L4, bypass de WAF/filtros,
  evidencia reproducible, jamás destructivo sin aprobación.
- **P1.8 Reporting** — CVSS 3.1 + CWE, plantillas de informe, redacción de evidencia.

### P2. Blue Team / Defensa

- **P2.1 Monitoreo y detección** — Suricata/Zeek, reglas Snort/Suricata, SIEM,
  correlación, dashboards.
- **P2.2 Threat hunting** — hipótesis, búsqueda en logs, MITRE ATT&CK mapping.
- **P2.3 Incident Response** — playbooks, triaje, contención, erradicación,
  recuperación, lecciones aprendidas.
- **P2.4 Forense** — adquisición y análisis de imagen, memória/volatilidad, artefactos
  de sistema, timeline, análisis de malware básico.
- **P2.5 Hardening** — CIS Benchmarks, config segura de Linux/Windows, endurecimiento
  de servicios, gestión de parches, antimalware.
- **P2.6 Threat Intelligence** — fuentes CTI, IOC extracción, TTPs, informes.
- **P2.7 Supply-chain forensics / OSINT forense** — investigación de repos open-source
  (compromiso de maintainer, dependencia maliciosa, force-push, credenciales borradas);
  extracción/enriquecimiento de IOCs; recuperación de commits/PR/issues vía git fsck,
  GitHub API, Wayback y GH Archive. Tarjetas en `skills/FORENSE/`.

### P3. Cumplimiento / Compliance

- **P3.1 Marcos normativos** — ISO/IEC 27001/27002, NIST CSF 2.0, CIS Controls,
  GDPR/LOPDGDD, PCI-DSS, ENS (España), NIS2/DORA, SOC 2.
- **P3.2 Gestión de riesgos** — riesgo/tratamiento, inventario de activos,
  análisis de impacto, métricas.
- **P3.3 Controles** — catálogo de controles, implementación, políticas, SGSI.
- **P3.4 Auditoría** — plan de auditoría, recolección de evidencia, hallazgos,
  planes de acción, remediación.
- **P3.5 Evaluación de terceros** — due diligence de proveedores, DPA.

### P4. Fundamentos y Ops

- **P4.1 Operación Kali-WSL** — bridge `wsl -d kali-linux`, instalación de tools,
  actualizaciones, gestión de paquetes.
- **P4.2 Scripting** — bash + python3 para automatizar recon/parsing/logs.
- **P4.3 Documentación** — estructura de engagements, evidencia, plantillas.
  Subskills desplegadas en `skills/<AREA>/` (INDEX + tarjetas destiladas), fuente
  completa en `skills/_src/` (ver `KB-SKILLS.md`).
- **P4.4 Metodología del agente** — guardrails, clasificación L1–L4, redacción
  de reportes con lenguaje preciso.

## Estado de cobertura (a completar con nuevas skills)

| Sublista | Estado |
|---|---|
| P1.1, P1.8, P2.7 | Cobertura OSINT/FORENSE vía skill sherlock + oss-forensics (desplegadas en `skills/OSINT/` y `skills/FORENSE/`) |
| P1.2–P1.3, P1.5, P1.7 | Cobertura por pack recon-skills + tarjetas (REDES/WEB/REDTEAM) + SKILL-AD |
| P1.4, P1.6 | Toolset instalado (Metasploit, hydra, aircrack); falta validar en labs |
| P2.1–P2.6 | Desplegado: 15 tarjetas BLUETEAM (Sigma, Elastic, Chainsaw, DCSync, Splunk, Golden Ticket, LOLBins, Wazuh, SOAR, ransomware, purple team, Velociraptor, SIEM) |
| P3.1–P3.5 | Desplegado: 10 tarjetas CUMPLIMIENTO (cmmc, iso27001, pcidss, gdpr, nist-rmf, riesgo-80030, nist-csf, soc2, tpv, nerc-cip) |
| P4.1–P4.4 | Operativo vía AGENTS.md y estructura `skills/` |

## Próximos pasos

- Recibir nuevas skills del usuario → registrar en `KB-SKILLS.md` y profundizar
  la sublista correspondiente; ampliar `skills/<AREA>/` con nuevas tarjetas.
