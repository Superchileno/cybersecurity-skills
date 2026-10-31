# Avisos de terceros (THIRD-PARTY-NOTICES)

Este repositorio incluye, bajo `skills/_src/`, código y documentación de
terceros. Se reproducen aquí las licencias correspondientes. Las **tarjetas
destiladas** (`skills/<AREA>/SKILL-*.md`) y los `INDEX.md` son obra propia de
este proyecto y se distribuyen bajo MIT (ver `LICENSE`), salvo que referencien
fuentes de terceros (que conservan su licencia original).

---

## 1) `skills/_src/hermes-security/` — Hermes Agent (Nous Research)

Skills oficiales del ecosistema Hermes Agent (`security/web-pentest`,
`security/oss-forensics`, `security/sherlock`). Origen:
https://hermes-ai.net/skills y repos oficiales de Nous Research.

- **Licencia**: la propia del ecosistema Hermes Agent (ver los repositorios
  oficiales de Nous Research). Este repositorio las incluye como **muestra
  educativa** para referencia.
- **Atribución**: Hermes Agent, Nous Research.
- **Uso**: consultar los repos oficiales para los términos completos.

## 2) `skills/_src/recon-skills/` — uphiago/recon-skills (MIT)

145 skills fuente del pack **recon-skills**. Origen:
https://github.com/uphiago/recon-skills

Licencia **MIT** (se reproduce el texto que acompaña al pack):

```
MIT License

Copyright (c) 2025 Hiago Felipe

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 3) `skills/_src/mukul-anthropic/` — mukul975/Anthropic-Cybersecurity-Skills (Apache-2.0)

54 skills curadas (de un total de 817) del repositorio
**Anthropic-Cybersecurity-Skills**. Origen:
https://github.com/mukul975/Anthropic-Cybersecurity-Skills

- **Licencia**: Apache License 2.0 (según su repositorio de origen).
- **Atribución**: mukul975 / Anthropic-Cybersecurity-Skills.
- **Nota**: cada skill incluye su `SKILL.md` y, donde aplica, subcarpetas
  `references/` y `scripts/`. No se incluye aquí el texto completo de la
  licencia Apache-2.0; referirse al repositorio de origen.

## 4) `skills/CTF/` — obra propia derivada

Las 7 tarjetas ejecutables del área CTF y sus skills completas en
`skills/CTF/_full/` son **obra propia** de este proyecto, derivadas de la
resolución de desafíos en competiciones de CTF reales.

- **Licencia**: MIT (igual que el resto de tarjetas propias).
- **Sanitización**: el contenido publicado fue procesado con `tools/sanitize.py`
  para eliminar flags, hosts, direcciones IP, credenciales, shortlinks y nombres
  de retos. Se conserva únicamente la técnica, los comandos y las lecciones.
- **Scripts**: los `scripts/` del área CTF son genéricos y parametrizables; no
  contienen datos de objetivos reales.
- **Limitación**: no se publican writeups con flags de eventos activos. Si se
  añaden casos de estudio, deben sanearse antes de commitear
  (`python tools/sanitize.py --path <ruta> --check`).

---

## 5) `skills/_src/ljagiello-ctf-skills/` — ljagiello/ctf-skills (MIT)

Material de profundidad para las categorías CTF que este proyecto no cubría.
Origen: https://github.com/ljagiello/ctf-skills

- **Commit vendorizado**: `a6106aaf5f1f4eeb6b95908f11c2314c7150dfac`
  (2026-10-30). Ver `skills/_src/ljagiello-ctf-skills/VENDOR.md`.
- **Autor original**: Lukasz Jagiello.
- **Licencia**: MIT. El texto completo está en
  `skills/_src/ljagiello-ctf-skills/LICENSE`.
- **Alcance copiado**: `ctf-web/`, `ctf-misc/`, `ctf-ai-ml/`, `ctf-malware/`,
  `ctf-osint/`, `solve-challenge/`, `ctf-writeup/`, `ctf-similar-search/` y
  `scripts/install_ctf_tools.sh`.
- **No copiado**: `.github/`, `evals/`, `tests/`, `pyproject.toml`, metadatos de
  su proyecto y los scripts de infraestructura (`generate_catalog.py`,
  `skill_security_auditor.py`, `verify_crypto_examples.py`). Tampoco se
  vendorizaron `ctf-pwn/`, `ctf-crypto/`, `ctf-reverse/` ni `ctf-forensics/`,
  que este repositorio cubre con material propio.
- **Modificaciones locales**: ninguna sobre el contenido técnico. Se añadió
  `VENDOR.md` (procedencia y alcance) y no se alteraron los archivos originales.
- **Saneamiento**: revisado con `tools/sanitize.py` y búsqueda dirigida de
  flags. El único texto con forma de flag es un marcador explícitamente falso
  (`MetaCTF{fake_banner_flag_here}`) del material original.
- **Uso**: `scripts/install_ctf_tools.sh` se conserva como referencia y **no se
  ejecuta** desde este repositorio.

Las tarjetas puente `SKILL-CTF-{WEB,MISC,AI-ML,MALWARE,OSINT,ORQUESTACION}.md`
son obra propia: resumen la técnica en español y enrutan al material anterior.

---

## Resumen

| Pack | Origen | Licencia | Incluido |
|---|---|---|---|
| hermes-security | Nous Research / hermes-ai.net | propia de Hermes | `skills/_src/hermes-security/` |
| recon-skills | uphiago/recon-skills | MIT | `skills/_src/recon-skills/` |
| mukul-anthropic | mukul975/Anthropic-Cybersecurity-Skills | Apache-2.0 | `skills/_src/mukul-anthropic/` |
| ljagiello-ctf-skills | ljagiello/ctf-skills | MIT | `skills/_src/ljagiello-ctf-skills/` |
| CTF | Obra propia (derivada de retos resueltos, saneada) | MIT | `skills/CTF/` |

Si reproducís o modificás cualquiera de estos packs, respetá las licencias
originales e indicá las modificaciones.