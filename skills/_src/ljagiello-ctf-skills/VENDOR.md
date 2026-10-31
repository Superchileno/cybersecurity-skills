# Material vendorizado — ljagiello/ctf-skills

- Origen: https://github.com/ljagiello/ctf-skills
- Licencia: MIT (ver `LICENSE` en esta carpeta)
- Commit vendorizado: a6106aaf5f1f4eeb6b95908f11c2314c7150dfac
- Fecha del commit: 2026-10-30T09:48:52-07:00
- Autor original: Lukasz Jagiello

## Alcance

Se copiaron sin modificar de fondo: `ctf-web/`, `ctf-misc/`, `ctf-ai-ml/`,
`ctf-malware/`, `ctf-osint/`, `solve-challenge/`, `ctf-writeup/`,
`ctf-similar-search/` y `scripts/install_ctf_tools.sh`.

Se excluyeron por ser infraestructura del proyecto original: `.github/`,
`evals/`, `tests/`, `pyproject.toml`, `CITATION.cff`, `CODE_OF_CONDUCT.md`,
`CONTRIBUTING.md`, `SECURITY.md`, `scripts/generate_catalog.py`,
`scripts/skill_security_auditor.py`, `scripts/verify_crypto_examples.py`.

No se vendorizaron `ctf-pwn/`, `ctf-crypto/`, `ctf-reverse/` ni
`ctf-forensics/`: este repositorio mantiene cobertura propia con scripts
ejecutables en `skills/CTF/_full/`.

## Uso

Este árbol es material de profundidad. No es una skill instalable por sí mismo:
las tarjetas `skills/CTF/SKILL-CTF-{WEB,MISC,AI-ML,MALWARE,OSINT,ORQUESTACION}.md`
enrutan hacia aquí, y `scripts/install_skills.py --with-deep` copia los `.md` a
`references/` de la skill instalada.

`scripts/install_ctf_tools.sh` es el instalador de toolchain del proyecto
original. Se conserva como referencia; **no se ejecuta** desde aquí.

## Actualizar

```bash
git clone --depth 1 https://github.com/ljagiello/ctf-skills.git /tmp/ljagiello
git -C /tmp/ljagiello rev-parse HEAD    # anotar el nuevo SHA en este archivo
```

Después repetir la copia selectiva y regenerar el manifiesto.
