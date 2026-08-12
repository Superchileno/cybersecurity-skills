# FORENSE — Subskills de forense digital

Área: forense de supply-chain en repositorios, recuperación de commits, análisis
de evidencia, cadena de custodia, forense de memoria/disco/timelines y análisis
de malware. Fuente completa: `skills/_src/hermes-security/oss-forensics`,
`skills/_src/mukul-anthropic/*`.

## Subskills destiladas

| Subskill | Cuándo usarla | Fuente |
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

## Metodología núcleo (oss-forensics, 7 fases)

1. Inicialización → 2. Extracción de IOCs → 3. Recogida de evidencia en
   paralelo (git local, GitHub API, Wayback, GH Archive/BigQuery, enriquecimiento)
   → 4. Consolidación → 5. Hipótesis → 6. Validación → 7. Informe forense.

## Guardrails anti-hallucination (extraídos de la skill)

- Toda afirmación en el informe cita un evidencia ID (`EV-XXXX`).
- Marcar hipótesis como `[HYPOTHESIS]` hasta validarlas.
- Doble verificación SHA/URL con 2+ fuentes.
- Nunca ejecutar código sospechoso del repo investigado (análisis estático o sandbox).
- Redactar secretos/tokens. Uso ético: nada de doxing ni acoso.

## Recuerda (guardrails)

- Forense = defensivo; requiere autorización del repositorio que se investiga.