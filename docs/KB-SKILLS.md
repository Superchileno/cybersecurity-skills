# KB-SKILLS.md — Inventario de skills (adoptadas / referencia)

Registro de skills del ecosistema analizadas, adoptadas y pendientes. Fuentes:
hermes-ai.net/skills, repos `NousResearch/hermes-agent` (optional-skills/security),
pack `uphiago/recon-skills` (MIT), HermesAtlas (hermesatlas.com),
`mukul975/Anthropic-Cybersecurity-Skills` (Apache-2.0).

## Adoptadas / de referencia

| Skill | Fuente | Estado | Ubicación / Uso |
|---|---|---|---|
| security/web-pentest | Hermes Agent (official) | Adoptada | `skills/_src/hermes-security/web-pentest` + destilada `skills/WEB/SKILL-WEBPENTEST.md` |
| oss-forensics | Hermes Agent (official) | Adoptada | `skills/_src/hermes-security/oss-forensics` + destiladas `skills/FORENSE/*` |
| sherlock | Hermes Agent (official) | Adoptada | `skills/_src/hermes-security/sherlock` + destilada `skills/OSINT/SKILL-SHERLOCK.md` (sherlock-project 0.16.0 instalado en Kali) |
| recon-skills | uphiago/recon-skills (MIT) | Adoptada (fuente completa) | `skills/_src/recon-skills/` (145 SKILL.md). INDEX por área en `skills/<AREA>/INDEX.md` |
| Anthropic-Cybersecurity-Skills | mukul975/Anthropic-Cybersecurity-Skills (Apache-2.0) | Adoptada (54 curadas de 817) | `skills/_src/mukul-anthropic/` (54 SKILL.md + refs/scripts). Ver desglose abajo |
| dogfood | Hermes built-in | Referencia | QA web con evidencia; útil para blue team web (ver `KB-CIBERSEGURIDAD.md` P2) |
| godmode (jailbreak LLMs) | Hermes Agent (official) | NO adoptada | Solo referencia; choca con guardrails de AGENTS.md (AI red-team) |
| 1password / unbroker | Hermes Agent (official) | No adoptada | Gestión de secretos / OTC; fuera del alcance del rol por ahora |

### Desglose de las 54 skills de `_src/mukul-anthropic/`

Tarjeta destilada por skill, agrupadas por área:

- **CUMPLIMIENTO (10)**: cmmc, iso27001, pcidss, gdpr, nist-rmf, riesgo-80030,
  nist-csf, soc2, tpv, nerc-cip → `skills/CUMPLIMIENTO/`
- **BLUETEAM (15)**: sigma, hunting-elastic, beacons, chainsaw, dcsync,
  lateral-splunk, golden-ticket, lotl, wazuh, soar-phantom, playbook-ransomware,
  purple-team, velociraptor, siem-use-cases → `skills/BLUETEAM/`
- **FORENSE (13)**: volatility, autopsy, hayabusa, kape, dd-adquisicion, hindsight,
  zimmerman, plaso, foremost, ghidra, rootkits, yara → `skills/FORENSE/`
- **REDTEAM (6)**: c2-sliver, c2-havoc, c2-redirect, privesc-linux, eternalblue,
  entra-attack → `skills/REDTEAM/`
- **WEB (4)**: thick-client, xml-injection, hpp, prompt-leak → `skills/WEB/`
- **REDES (4)**: ct-logs, bgp-hijack, ssl-tls, shodan → `skills/REDES/`
- **OSINT (2)**: spiderfoot, actor-osint → `skills/OSINT/`

## Estructura de skills desplegadas (workspace)

```
skills/
├─ _src/recon-skills/        clon fuente completa (145 SKILL.md originales)
├─ _src/hermes-security/     web-pentest, oss-forensics, sherlock (SKILL.md oficiales)
├─ _src/mukul-anthropic/     54 skills curadas del repo mukul975 (Apache-2.0)
├─ REDTEAM/                  INDEX + tarjetas: metodología, pwspray, evidencia,
│                            reporte, cadenas, AD + c2-sliver/havoc/redirect,
│                            privesc-linux, eternalblue, entra-attack
├─ REDES/                    INDEX + tarjetas: subdominios, puertos, vhost,
│                            fingerprint, origen-IP + ct-logs, bgp-hijack, ssl-tls, shodan
├─ WEB/                      INDEX + tarjetas: webpentest, enum-web, sqli, xss, ssrf,
│                            lfi-rce, upload, idor-ato, wpscan, api + thick-client,
│                            xml-injection, hpp, prompt-leak
├─ OSINT/                    INDEX + tarjetas: sherlock, osint, secretos, gdorks
│                            + spiderfoot, actor-osint
├─ BLUETEAM/                 INDEX + tarjetas: 15 subskills de defensa (Sigma,
│                            Elastic, Cobalt Strike, Chainsaw, DCSync, Splunk,
│                            Golden Ticket, LOLBins, Wazuh, SOAR, ransomware,
│                            purple team, Velociraptor, SIEM)
├─ FORENSE/                  INDEX + tarjetas: oss-forensics, recuperar, ioc
│                            + volatility, autopsy, hayabusa, kape, dd, hindsight,
│                            zimmerman, plaso, foremost, ghidra, rootkits, yara
└─ CUMPLIMIENTO/             INDEX + tarjetas: cmmc, iso27001, pcidss, gdpr,
                             nist-rmf, riesgo-80030, nist-csf, soc2, tpv, nerc-cip
```

Cada área tiene un `INDEX.md` con "cuándo usar qué" y enrutado al `_src` para
profundizar. Las tarjetas son destiladas (token-friendly) y respetan los
guardrails de `AGENTS.md`.

## Hubs de skills

- **agentskills.io** — hub comunitario compatible con formato Hermes (88k+ skills
  indexadas; 403 scraping directo, acceder por navegador/API).
- **HermesAtlas** — 817 skills de ciberseguridad, 29 dominios, mapeadas a 6
  frameworks (ISO/NIST/OWASP/etc.).
- **Repos oficiales/community** — `NousResearch/hermes-agent` (optional-skills),
  `uphiago/recon-skills`, skillhub.cn, xiaping.coze.com.

## Huecos detectados (candidatos a nuevas skills)

1. **AD avanzado**: bloodhound, kerberoasting (cobertura básica en `SKILL-AD.md`),
   movimiento lateral (parcial: DCSync/golden ticket en BLUETEAM; exploits en REDTEAM).
2. **Wireless**: suite aircrack (solo alcance aprobado).
3. **Cloud L4**: k8s/misconfig / cloud IAM (parcial en `_src/recon-skills`).
4. **Blue Team avanzado**: hardening CIS, TI/Hunt, IR playbooks (base ya en BLUETEAM).

## Registro de nuevas skills (dejar aquí las que aporte el usuario)

- (pendiente)

## Criterio de adopción

- Compatible con el rol (pentesting/blue/compliance/ops).
- Guardrails compatibles con AGENTS.md (autorización, alcance, no destructivo).
- Si una skill choca con los guardrails → se adapta o se rechaza (caso `godmode`).