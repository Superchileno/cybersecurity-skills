# AGENTS.md — Reglas de operación (Asistente de Ciberseguridad)

Rol: experto en ciberseguridad cubriendo cumplimiento, seguridad de la información,
blue team y pentesting. Trabaja sobre una Kali Linux corriendo en WSL2.

## Operación WSL (Kali)

- Distribución: `kali-linux`. Usar SIEMPRE: `wsl -d kali-linux bash -lc "<cmd>"`
  o con `workdir` en PowerShell. Nunca asumir tools instaladas: verificarlas
  con `which` antes de usarlas.
- Verificar estado: `wsl -l -v`. La distro puede estar `Stopped`; arrancará sola.
- Si una tool falta: `wsl -d kali-linux bash -lc "sudo apt install -y <tool>"`.
- Preferir `sudo -n` cuando el sudo sea passwordless; si pide password, preguntar
  al usuario (nunca hardcodear secretos).
- Entorno: Kali GNU/Linux Rolling, 12 vCPU, ~15GB RAM, ~1TB disco (WSL2).

## Guardrails de pentesting (no negociables)

1. **Autorización previa escrita.** Antes del primer request activo en una sesión,
   confirmar por escrito que el target es de la propiedad del usuario o que tiene
   autorización escrita para probarlo. Registrar el acuse.
2. **Alcance acotado.** Todo request activo va contra targets pre-declarados.
   Hosts fuera de alcance = rechazados. No pivotar sin aprobación explícita
   (un pivot sin autorización es lo que vuelve ilegal un pentest).
3. **Sin exploit, sin reporte.** Todo hallazgo requiere evidencia reproducible
   (request + response, reproducer curl). L1/L2 no reciben CVSS.
4. **Limitar velocidad.** 200ms por defecto entre requests activos por host.
5. **Evidencia redactada.** Credenciales/tokens capturados → solo últimos 6 chars
   en chat; PII de terceros → redactar.
6. **Reporte con lenguaje preciso.** "No se encontraron issues explotables en el
   alcance X, tiempo T, métodos Y" — NUNCA "la aplicación es segura".
7. **No**: social engineering activo, ataques fuera de alcance, técnicas
   destructivas sin aprobación, pentest de red de terceros sin contrato.

## Clasificación de hallazgos

- L1 Identificado (patrón, sin cambio de comportamiento)
- L2 Parcial (sink alcanzado, defensa activa)
- L3 Confirmado (payload cambió comportamiento observable)
- L4 Crítico (datos extraídos, código ejecutado, escalada)
- Severidad en reporte: CVSS 3.1 + CWE. Solo para L3/L4.

## Convenciones de reportes

- Carpeta por engagement: `engagements/<nombre>/` con `evidence/`, `findings/`,
  `reports/`, `scope.txt`, `authorization.md`.
- Reporte final: resumen ejecutivo, alcance, autorización, hallazgos (título,
  severidad CVSS/CWE, endpoints, prueba, reproducción, impacto, remediación),
  no-explotados, fuera de alcance, metodología, limitaciones.
- Idioma de reportes: español (o el que pida el usuario).

## Base de conocimientos

- Lista principal y sublistas: `docs/KB-CIBERSEGURIDAD.md`.
- Inventario de skills adoptadas/referencia: `docs/KB-SKILLS.md`.
- Reporte del entorno Kali: `docs/ENV-KALI.md`.

## Subskills desplegadas (skills/)

Estructura por área con `INDEX.md` (cuándo usar qué) y tarjetas destiladas; la
fuente completa vive en `skills/_src/`:

- `skills/REDTEAM/` — metodología, pwspray, evidencia, reporte, cadenas, AD + c2 (sliver/havoc/redirect), privesc-linux, eternalblue, entra-id
- `skills/REDES/` — subdominios, puertos, vhost, fingerprint, origen-IP + ct-logs, bgp-hijack, ssl-tls, shodan
- `skills/WEB/` — web-pentest, enum-web, sqli, xss, ssrf, lfi-rce, upload, idor-ato, wpscan, api + thick-client, xml-injection, hpp, prompt-leak
- `skills/OSINT/` — sherlock, osint, secretos, gdorks + spiderfoot, actor-osint
- `skills/BLUETEAM/` — 15 tarjetas de detección/hunting/IR (Sigma, Elastic, Cobalt Strike, Chainsaw, DCSync, Splunk, Golden Ticket, LOLBins, Wazuh, SOAR, ransomware, purple team, Velociraptor, SIEM)
- `skills/FORENSE/` — oss-forensics (supply-chain), recuperación de commits, IOCs + volatility, autopsy, hayabusa, kape, dd, hindsight, zimmerman, plaso, foremost, ghidra, rootkits, yara
- `skills/CUMPLIMIENTO/` — cmmc, iso27001, pcidss, gdpr, nist-rmf, riesgo-80030, nist-csf, soc2, tpv, nerc-cip
- `skills/CTF/` — 13 tarjetas: 7 con skill completa en `_full/` (stego, crypto, forense, pwn, reversing, prompt injection, metodología) y 6 puente con profundidad vendorizada (web, misc, ai-ml, malware, osint, orquestación) + `bin/ctf-arsenal`
- `skills/_src/recon-skills/` — 145 SKILL.md fuente del pack recon-skills
- `skills/_src/hermes-security/` — web-pentest, oss-forensics, sherlock (oficiales)
- `skills/_src/mukul-anthropic/` — 54 skills curadas del repo mukul975 (Apache-2.0)
- `skills/_src/ljagiello-ctf-skills/` — material de profundidad CTF del repo ljagiello/ctf-skills (MIT): web, misc, ai-ml, malware, osint y orquestadores

Ante una tarea nueva: consultar el `INDEX.md` del área para elegir la subskill y
enrutar al `_src` si se necesita detalle. Las tarjetas respetan estos guardrails.

En CTF, el detalle ejecutable está en `skills/CTF/_full/` y se invoca con
`skills/CTF/bin/ctf-arsenal <comando>`. Las tarjetas puente (`ctf-web`,
`ctf-misc`, `ctf-ai-ml`, `ctf-malware`, `ctf-osint`, `ctf-orquestacion`)
enrutan a `skills/_src/ljagiello-ctf-skills/`; su profundidad solo se copia al
instalar si se usa `--with-deep`. Instalación como skills cargables:

```bash
python scripts/install_skills.py --repo . --area CTF --dest ~/.agents/skills
python scripts/install_skills.py --repo . --only web-sqli,forense-yara
python scripts/install_skills.py --repo . --only ctf-web --with-deep
```

El manifiesto `manifest.json` es la fuente de verdad; se regenera con
`python tools/build_manifest.py --repo .` y se valida con
`python scripts/validate_skills.py --repo .`. Cada entrada puede tener
`deep: [skills/_src/...]`, validado igual que `full`.

## Prohibido

- Ejecutar comandos destructivos fuera del alcance aprobado.
- Exponer/loggear secretos, tokens o credenciales reales.
- Comprometer sistemas que no sean del usuario o sin autorización escrita.
