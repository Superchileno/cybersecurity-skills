# REDTEAM — Subskills de pentest ofensivo

Área: explotación, cadenas de ataque, metodología ofensiva, movimiento lateral.
Fuente completa: `skills/_src/recon-skills/redteam/*`, `skills/_src/recon-skills/chains/*`,
`skills/_src/mukul-anthropic/*`.

## Subskills destiladas

| Subskill | Cuándo usarla | Fuente |
|---|---|---|
| `SKILL-METODOLOGIA.md` | Antes de todo engagement: mindset, enfoque, expansión de sector | `redteam/redteam-mindset`, `redteam/recon-sector`, `bb-methodology` |
| `SKILL-PWSPRAY.md` | Login brute-force sutil por emplazamiento con bloqueos | `redteam/password-spray-methodology` |
| `SKILL-EVIDENCIA.md` | Capturar evidencia reproducible y redactada (guardrails AGENTS.md) | `redteam/evidence-hygiene` |
| `SKILL-REPORTE.md` | Escribir reporte profesional (CVSS/CWE, plantilla) | `redteam/report-writing`, `redteam/redteam-report-template` |
| `SKILL-CADENAS.md` | Construir cadenas de ataque evidencing-based (cross-attack-chains) | `chains/cross-attack-chains` |
| `SKILL-AD.md` | Pentest Active Directory: enums, kerberoasting, mov. lateral | toolset netexec/impacket + `mukul-anthropic` AD | 
| `SKILL-C2-SLIVER.md` | Operar C2 con Sliver | `mukul-anthropic/operating-sliver-c2` |
| `SKILL-C2-HAVOC.md` | Operar C2 con Havoc | `mukul-anthropic/operating-havoc-c2` |
| `SKILL-C2-REDIRECT.md` | Infraestructura de redirección C2 | `mukul-anthropic/building-c2-redirector-infrastructure` |
| `SKILL-PRIVESC-LINUX.md` | Escalada de privilegios Linux | `mukul-anthropic/performing-privilege-escalation-on-linux` |
| `SKILL-ETERNALBLUE.md` | Explotar MS17-010 (EternalBlue/SMB) | `mukul-anthropic/exploiting-ms17-010-eternalblue-vulnerability` |
| `SKILL-ENTRA-ATTACK.md` | Atacar Entra ID / M365 (roadtools, GraphRunner) | `mukul-anthropic/attacking-entra-id-with-roadtools`, `post-exploiting-microsoft-graph-with-graphrunner` |

## Enrutado al _src (para detalle por clase de vuln)

- Vector AI/LLM: `redteam/llm-prompt-injection`, `hunt-llm-ai` | `redteam/mcp-security` en `hunt-mcp-security`
- M365/Entra/Okta: `redteam/m365-entra-attack`, `redteam/okta-attack`
- Infra virtualizada: `redteam/vmware-vcenter-attack`, `infra/docker-privesc`
- Bug bounty: `redteam/bug-bounty`, `redteam/bb-methodology`, `redteam/bugcrowd-reporting`
- Triage: `redteam/triage-validation` (validar antes de reportar)

## Recuerda (guardrails)

- Solo targets autorizados (ver `AGENTS.md`).
- Sin exploit, sin reporte: cada hallazgo requiere evidencian reproducible.
- L3/L4 únicamente reciben CVSS + CWE.