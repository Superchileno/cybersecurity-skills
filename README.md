# 🔐 cybersecurity-skills — Biblioteca de habilidades de ciberseguridad

Colección de **80 tarjetas de habilidades** (skills) listas para usar por un
asistente de IA en tareas de ciberseguridad: cumplimiento, seguridad de la
información, blue team y pentesting. Cada tarjeta es un archivo Markdown
estructurado (`SKILL-*.md`) que distila el "cuándo usarla", el procedimiento,
la clasificación de hallazgos, las herramientas y los *guardrails*.

> ⚠️ **Uso responsable.** Este repositorio es material educativo y operativo
> para profesionales y estudiantes de seguridad. Solo úsalo contra sistemas
> propios o con **autorización escrita** previa. Ver `AGENTS.md`.

---

## 📁 Contenido

| Área | Tarjetas | Cobertura |
|---|---|---|
| [`skills/REDTEAM/`](skills/REDTEAM/INDEX.md) | 12 | Pentest ofensivo, cadenas de ataque, C2, AD |
| [`skills/REDES/`](skills/REDES/INDEX.md) | 9 | Recon de red, puertos, vhosts, TLS, BGP |
| [`skills/WEB/`](skills/WEB/INDEX.md) | 14 | Clases de vuln web, APIs, LLM, thick clients |
| [`skills/OSINT/`](skills/OSINT/INDEX.md) | 6 | Recon pasivo, secretos, actores, dorks |
| [`skills/BLUETEAM/`](skills/BLUETEAM/INDEX.md) | 14 | Detección, hunting, SIEM, SOAR, IR |
| [`skills/FORENSE/`](skills/FORENSE/INDEX.md) | 15 | Memoria, disco, timelines, malware, YARA |
| [`skills/CUMPLIMIENTO/`](skills/CUMPLIMIENTO/INDEX.md) | 10 | Marcos normativos y gestión de riesgo |
| `docs/` | — | Formato, catálogo y KB del proyecto |
| `skills/_src/` | — | Fuentes completas (packs de terceros) |

**Catálogo detallado de las 80 tarjetas:** [`docs/CATALOGO-SKILLS.md`](docs/CATALOGO-SKILLS.md)

---

## 🧩 Estructura de una tarjeta

```
skills/<AREA>/
├─ INDEX.md            # "cuándo usar qué" + enrutado al _src
├─ SKILL-<SLUG>.md     # tarjeta destilada
└─ ...
```

Cada área tiene un `INDEX.md` que actúa como índice de navegación. Las tarjetas
siguen un **formato fijo de 6 secciones** (especificación completa:
[`docs/FORMATO-SKILLS.md`](docs/FORMATO-SKILLS.md)):

1. `# SKILL-<SLUG>.md — Título`
2. `## Cuándo usarla`
3. `## Procedimiento resumido`
4. `## Clasificación de hallazgo` (opcional)
5. `## Herramientas Kali`
6. `## Guardrails`

---

## 📥 Cómo usar estas skills

Requisitos:

- Un asistente de IA / agente que cargue skills desde archivos Markdown
  (p. ej. Claude, opencode, o cualquier rig compatible con el formato
  `skill`/`SKILL.md`).
- **Kali Linux / WSL2 recomendado**: muchas herramientas listadas viven en
  el ecosistema Kali (`nmap`, `sqlmap`, `burpsuite`, `hashcat`, `netexec`,
  `impacket`, `wpscan`, etc.). Ver [`docs/ENV-KALI.md`](docs/ENV-KALI.md).
- Usuarios de Windows/macOS: las tarjetas mencionan herramientas; instala
  las equivalentes en tu plataforma.

Pasos rápidos:

```bash
git clone https://github.com/superchileno/cybersecurity-skills.git
cd cybersecurity-skills
# Revisa el INDEX del área que necesites, p. ej.:
less skills/REDTEAM/INDEX.md
# Carga la tarjeta concreta en tu agente:
cat skills/REDES/SKILL-SUBDOMINIOS.md
```

Para **crear tus propias tarjetas** siguiendo el mismo formato: leer
[`docs/FORMATO-SKILLS.md`](docs/FORMATO-SKILLS.md).

---

## 🧠 Base de conocimientos del proyecto

- [`docs/KB-CIBERSEGURIDAD.md`](docs/KB-CIBERSEGURIDAD.md) — pilares del
  know-how: OSINT, red team, blue team, cumplimiento y operación (P1–P4).
- [`docs/KB-SKILLS.md`](docs/KB-SKILLS.md) — inventario de skills adoptadas,
  fuentes y criterio de adopción.
- [`docs/ENV-KALI.md`](docs/ENV-KALI.md) — reporte del entorno Kali usado
  (toolset instalado y versiones).
- [`AGENTS.md`](AGENTS.md) — reglas de operación y guardrails del asistente.

---

## 📚 Atribución de fuentes (`skills/_src/`)

El repositorio incluye las fuentes completas de tres packs de terceros con su
respectiva licencia. Detalle en
[`THIRD-PARTY-NOTICES.md`](THIRD-PARTY-NOTICES.md):

| Pack | Origen | Licencia |
|---|---|---|
| `_src/hermes-security/` | Hermes Agent (Nous Research) — skills oficiales web-pentest, oss-forensics, sherlock | propia de Hermes (ver origen) |
| `_src/recon-skills/` | [uphiago/recon-skills](https://github.com/uphiago/recon-skills) (145 SKILL.md) | MIT |
| `_src/mukul-anthropic/` | [mukul975/Anthropic-Cybersecurity-Skills](https://github.com/mukul975/Anthropic-Cybersecurity-Skills) (54 skills curadas de 817) | Apache-2.0 |

Las **80 tarjetas destiladas** (`skills/<AREA>/SKILL-*.md`) y los `INDEX.md`
son obra de este proyecto y se distribuyen bajo **MIT** (ver [`LICENSE`](LICENSE)).

---

## 🛡️ Guardrails (no negociables)

1. **Autorización previa escrita** antes de cualquier request activo.
2. **Alcance acotado**; sin pivot sin aprobación explícita.
3. **Sin exploit, sin reporte**: todo hallazgo con evidencia reproducible.
4. Clasificación **L1–L4**; CVSS 3.1 + CWE solo para L3/L4.
5. Evidencia **redactada**: credenciales → últimos 6 chars; PII de terceros → oculto.
6. Lenguaje preciso en reportes: "no se encontraron issues explotables en X" ≠ "la app es segura".

---

## 📄 Licencia

- Tarjetas destiladas, `INDEX.md` y documentación: **MIT** — ver [`LICENSE`](LICENSE).
- Packs de terceros en `skills/_src/`: ver [`THIRD-PARTY-NOTICES.md`](THIRD-PARTY-NOTICES.md).