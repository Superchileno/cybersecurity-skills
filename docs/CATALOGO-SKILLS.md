# Catálogo de skills

Listado completo de las **87 tarjetas** de este repositorio, por área.
Cada fila: tarjeta, cuándo usarla y fuente de detalle (si aplica).

## REDTEAM — pentest ofensivo (12)

| Tarjeta | Cuándo usarla | Fuente |
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

## REDES — recon de red (9)

| Tarjeta | Cuándo usarla | Fuente |
|---|---|---|
| `SKILL-SUBDOMINIOS.md` | Enumeración pasiva/activa de subdominios | `recon/subdomain-enumeration`, `recon/subdomain-takeover-hunt` |
| `SKILL-PUERTOS.md` | Escaneo de puertos/servicios a escala y clasificación | `recon/port-mass-scan`, `recon/port-service-discovery` |
| `SKILL-VHOST.md` | Enumeración de virtual hosts | `recon/vhost-enumeration` |
| `SKILL-FINGERPRINT.md` | TLS fingerprint, HTTP/2 impersonation, camuflaje | `recon/tls-fingerprint-impersonation`, `recon/http2-header-impersonation` |
| `SKILL-ORIGEN-IP.md` | Descubrir IP real tras CDN/WAF (origin ip) | `recon/origin-ip-discovery` |
| `SKILL-CT-LOGS.md` | Analizar Certificate Transparency logs (subdominios pasivos, phishing) | `mukul-anthropic/analyzing-tls-certificate-transparency-logs` |
| `SKILL-BGP-HIJACK.md` | Evaluar hijacking BGP y mitigación RPKI | `mukul-anthropic/exploiting-bgp-hijacking-vulnerabilities`, `implementing-bgp-security-with-rpki` |
| `SKILL-SSL-TLS.md` | Auditar configuración TLS (testssl, cifrados, certs) | `mukul-anthropic/performing-ssl-tls-security-assessment` |
| `SKILL-SHODAN.md` | Reputación/enriquecimiento de IP con Shodan | `mukul-anthropic/performing-ip-reputation-analysis-with-shodan` |

## WEB — aplicaciones web (14)

| Tarjeta | Cuándo usarla | Fuente |
|---|---|---|
| `SKILL-WEBPENTEST.md` | Metodología completa faseada (autorización→recon→análisis→exploit→reporte) | `hermes-security/web-pentest/SKILL.md` (oficial) |
| `SKILL-ENUM-WEB.md` | Enumeración web: paths, ficheros, tecnología, source maps | `recon/web-enumeration`, `recon/js-secrets-extraction` |
| `SKILL-SQLI.md` | SQL injection (todos los tipos + bypass) | `redteam/hunt-sqli` |
| `SKILL-XSS.md` | XSS reflejado/almacenado/DOM (+ DOM advanced) | `redteam/hunt-xss`, `redteam/hunt-dom` |
| `SKILL-SSRF.md` | Server-Side Request Forgery | `redteam/hunt-ssrf` |
| `SKILL-LFI-RCE.md` | LFI, RCE, phpinfo→RCE | `redteam/hunt-lfi`, `redteam/hunt-rce`, `recon/phpinfo-to-rce` |
| `SKILL-UPLOAD.md` | File upload bypass | `redteam/hunt-file-upload` |
| `SKILL-IDOR-ATO.md` | IDOR / Account Takeover / auth bypass | `redteam/hunt-idor`, `redteam/hunt-ato`, `redteam/hunt-auth-bypass` |
| `SKILL-WPSCAN.md` | WordPress: plugins, XMLRPC, REST auth bypass (wpscan) | `recon/wordpress-plugin-hunt`, `recon/xmlrpc-exploitation`, `recon/wp-*` |
| `SKILL-API.md` | APIs: no-auth, GraphQL, misconfig | `redteam/hunt-graphql`, `redteam/hunt-api-misconfig`, `recon/api-noauth-hunt` |
| `SKILL-THICK-CLIENT.md` | Pentest de clientes gordos (escritorio) | `mukul-anthropic/performing-thick-client-application-penetration-test` |
| `SKILL-XML-INJECTION.md` | XXE / XML injection | `mukul-anthropic/testing-for-xml-injection-vulnerabilities` |
| `SKILL-HPP.md` | HTTP Parameter Pollution | `mukul-anthropic/performing-http-parameter-pollution-attack` |
| `SKILL-PROMPT-LEAK.md` | Fuga de system prompt en LLM | `mukul-anthropic/testing-for-system-prompt-leakage` |

## OSINT — recon pasivo (6)

| Tarjeta | Cuándo usarla | Fuente |
|---|---|---|
| `SKILL-SHERLOCK.md` | Encontrar cuentas de un username en 400+ plataformas | `hermes-security/sherlock/SKILL.md` (oficial) |
| `SKILL-OSINT.md` | Metodología OSINT ofensiva + expansión de sector | `redteam/offensive-osint`, `redteam/osint-methodology` |
| `SKILL-SECRETOS.md` | Caza de secretos/credenciales en repos públicos | `recon/github-secret-hunting`, `recon/hardcoded-credential-hunt` |
| `SKILL-GDORKS.md` | Google dorks / catálogos de dorks | `meta/google-dorks-catalog` |
| `SKILL-SPIDERFOOT.md` | OSINT automatizado multi-módulo (SpiderFoot) | `mukul-anthropic/performing-osint-with-spiderfoot` |
| `SKILL-ACTOR-OSINT.md` | Perfil de actor de amenazas desde OSINT/CTI | `mukul-anthropic/building-threat-actor-profile-from-osint` |

## BLUETEAM — defensa (14)

| Tarjeta | Cuándo usarla | Fuente |
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

## FORENSE — análisis de evidencia (15)

| Tarjeta | Cuándo usarla | Fuente |
|---|---|---|
| `SKILL-OSS-FORENSICS.md` | Investigar compromise de supply-chain en un repo GitHub | `hermes-security/oss-forensics/SKILL.md` (oficial) |
| `SKILL-RECUPERAR.md` | Recuperar commits/PR/issues "force-pushed" o borrados | `oss-forensics` refs: `recovery-techniques.md`, `git fsck` |
| `SKILL-IOC.md` | Extraer, enriquecer y rastrear IOCs (evidencia EV-XXXX) | `oss-forensics` refs: `evidence-types.md` |
| `SKILL-VOLATILITY.md` | Análisis de memoria (Volatility 2/3) | `mukul-anthropic/analyzing-memory-dumps-with-volatility`, `performing-memory-forensics-with-volatility3` |
| `SKILL-AUTOPSY.md` | Análisis de imágenes de disco con Autopsy | `mukul-anthropic/analyzing-disk-image-with-autopsy` |
| `SKILL-HAYABUSA.md` | Timelines forenses Windows con Hayabusa | `mukul-anthropic/generating-forensic-timelines-with-hayabusa` |
| `SKILL-KAPE.md` | Triage forense Windows con KAPE | `mukul-anthropic/triaging-windows-with-kape` |
| `SKILL-DD-ACQUISICION.md` | Adquisición de imagen con dd/dcfldd | `mukul-anthropic/acquiring-disk-image-with-dd-and-dcfldd` |
| `SKILL-HINDSIGHT.md` | Forense de navegador con Hindsight | `mukul-anthropic/analyzing-browser-forensics-with-hindsight` |
| `SKILL-ZIMMERMAN.md` | Artefactos Windows con suite EZTools | `mukul-anthropic/performing-windows-artifact-analysis-with-eric-zimmerman-tools` |
| `SKILL-PLASO.md` | Super timelines con Plaso | `mukul-anthropic/building-super-timelines-with-plaso` |
| `SKILL-FOREMOST.md` | File carving con foremost | `mukul-anthropic/performing-file-carving-with-foremost` |
| `SKILL-GHIDRA.md` | Reversing de malware con Ghidra | `mukul-anthropic/reverse-engineering-malware-with-ghidra` |
| `SKILL-ROOTKITS.md` | Análisis de bootkits/rootkits | `mukul-anthropic/analyzing-bootkit-and-rootkit-samples` |
| `SKILL-YARA.md` | Reglas YARA de detección | `mukul-anthropic/performing-yara-rule-development-for-detection` |

## CUMPLIMIENTO — gobernanza (10)

| Tarjeta | Cuándo usarla | Fuente |
|---|---|---|
| `SKILL-CMMC.md` | Preparar CMMC L2 / NIST 800-171 (industria defensa DoD) | `achieving-cmmc-level-2-compliance` |
| `SKILL-ISO27001.md` | Diseñar/auditar SGSI ISO/IEC 27001 | `implementing-iso-27001-information-security-management` |
| `SKILL-PCIDSS.md` | Cumplir/auditar PCI DSS (datos de tarjetas) | `implementing-pci-dss-compliance-controls` |
| `SKILL-GDPR.md` | Controles GDPR/LOPDGDD + gestión de DSAR | `implementing-gdpr-data-subject-access-request` |
| `SKILL-NIST-RMF.md` | NIST RMF / Authorization to Operate | `executing-nist-rmf-authorization-to-operate` |
| `SKILL-RIESGO-80030.md` | Evaluación de riesgo con NIST SP 800-30 | `conducting-cyber-risk-assessment-with-nist-800-30` |
| `SKILL-NIST-CSF.md` | Evaluación de madurez NIST CSF 2.0 | `performing-nist-csf-maturity-assessment` |
| `SKILL-SOC2.md` | Preparación de examen SOC 2 Type 2 | `performing-soc2-type2-audit-preparation` |
| `SKILL-TPV.md` | Gestión de riesgo de terceros | `managing-third-party-vendor-risk` |
| `SKILL-NERC-CIP.md` | Cumplimiento NERC CIP (sector eléctrico) | `implementing-nerc-cip-compliance-controls` |

## CTF — retos y explotación (7, con arsenal ejecutable)

| Tarjeta | Cuándo usarla | Skill completa |
|---|---|---|
| `SKILL-CTF-METODOLOGIA.md` | Punto de entrada: triaje, clasificación, writeup | `_full/solving-ctf-challenges-systematically` |
| `SKILL-CTF-STEGO.md` | Polyglots, LSB, OOXML, mosaicos, capas | `_full/analyzing-file-artifacts-for-steganography` |
| `SKILL-CTF-CRYPTO.md` | XOR, two-time pad, Vigenère, catálogos | `_full/solving-classical-and-custom-cryptography` |
| `SKILL-CTF-FORENSE.md` | Audio, CEF, pcap, MFT/USN | `_full/performing-ctf-forensics-on-audio-and-logs` |
| `SKILL-CTF-PWN.md` | Format string, ret2win, SROP, heap, kernel | `_full/exploiting-binary-vulnerabilities-in-ctf` |
| `SKILL-CTF-REVERSING.md` | Binarios stripped, tablas, VMs, oráculos | `_full/reversing-obfuscated-binaries-and-vms` |
| `SKILL-CTF-PROMPT-INJECTION.md` | Directivas ocultas dirigidas a agentes de IA | `_full/defending-against-prompt-injection-in-ctf-agents` |

Arsenal: `skills/CTF/bin/ctf-arsenal` (26 comandos, `--list`).

---

**Total: 87 tarjetas.** Para el detalle completo de cada fuente, ver
[`THIRD-PARTY-NOTICES.md`](../THIRD-PARTY-NOTICES.md) y `skills/_src/`.