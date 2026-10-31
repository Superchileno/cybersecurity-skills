# Formato de skills (especificación)

Documento de referencia que define el **formato de las tarjetas de habilidades**
de este repositorio. Su objetivo es doble:

1. Que cualquier persona pueda **entender** una tarjeta de un vistazo.
2. Que cualquier persona pueda **crear tarjetas nuevas** consistentes con el resto.

---

## 1) Directorio por área

```
skills/<AREA>/
├─ INDEX.md            # índice: "cuándo usar qué"
├─ SKILL-<SLUG>.md     # tarjetas destiladas
└─ ...
```

- `<AREA>`: `REDTEAM`, `REDES`, `WEB`, `OSINT`, `BLUETEAM`, `FORENSE`,
  `CUMPLIMIENTO` (nombres en mayúsculas).
- `SKILL-<SLUG>.md`: `<SLUG>` describe la habilidad en corto (ej. `SQLI`, `C2-SLIVER`,
  `HAYABUSA`). Sin espacios; usar guiones.

## 2) Archivo `INDEX.md`

Rol: navegación. Cada área tiene un `INDEX.md` con:

- Cabecera que describe el área y su cobertura.
- **Tabla de tarjetas** con columnas: `Subskill` (enlace a la tarjeta),
  `Cuándo usarla`, `Fuente`.
- Sección **Enrutado al `_src`**: cuándo ir al detalle completo del pack fuente.
- Sección **Recuerda (guardrails)** con las limitaciones específicas del área.

## 2.1) Frontmatter YAML — REQUERIDO

Toda tarjeta empieza con un bloque YAML que permite instalarla como skill
cargable por un agente:

```yaml
---
name: web-sqli
description: 'Qué hace y cuándo usarla. Keywords: SQL injection, SQLi, WAF bypass.'
area: WEB
tags: [sqli, injection, web]
source: _src/recon-skills/redteam/hunt-sqli
license: Apache-2.0
---
```

Reglas:

- `name` = `<área>-<slug>` en minúsculas (`web-sqli`, `forense-volatility`,
  `ctf-pwn`). Debe ser único en todo el repositorio.
- `description` ≤ 1024 caracteres, en español, con **keywords en inglés** al final
  para mejorar el enrutamiento del agente.
- `area` debe coincidir con la carpeta.
- `source` es opcional: `_src/...` para material de terceros o `_full/...` para
  skills completas del área CTF.
- El bloque se coloca **antes** del `# SKILL-...`; GitHub lo renderiza como tabla.
- El frontmatter es aditivo: no cambia las secciones 3.1–3.7.

## 3) Tarjeta `SKILL-<SLUG>.md`

Estructura fija (secciones en orden). Las secciones opcionales se omiten cuando
no aplica:

### 3.1. Encabezado — `#`
```
# SKILL-<SLUG>.md — Título descriptivo
```
Primera línea, título corto que dice qué hace la habilidad.

### 3.2. Fuente (opcional) — línea inmediata
```
Fuente: `_src/<pack>/<nombre-original>/`.
```
Permite rastrear el detalle completo. Se omite si la tarjeta es 100% propia.

### 3.3. `## Cuándo usarla` — REQUERIDO
Condiciones y señales que disparan el uso de la tarjeta. Responde: *¿cuándo
alguien necesitaría esto?*

### 3.4. `## Procedimiento resumido` — REQUERIDO
Pasos numerados (`1. 2. 3.`), concisos y accionables. Idealmente con el comando
o técnica clave. No es un artículo: es un *cheat-sheet* accionable.

### 3.5. `## Clasificación de hallazgo` — OPCIONAL
Mapea resultados observables a la clasificación **L1–L4** (ver `AGENTS.md`):
ej. "error en BD visible → L3; dump de datos → L4".

### 3.6. `## Herramientas Kali` — OPCIONAL
Lista de herramientas del ecosistema Kali (y alternativas) usadas en el
procedimiento.

### 3.7. `## Guardrails` — RECOMENDADO
Límites de seguridad/ética/operación aplicables a la tarjeta: autorización,
velocidad de requests, redacción de evidencia, no-destructivo.

## 4) Reglas de estilo

- **Markdown ligero**: encabezados `##`, listas, tablas. Sin HTML salvo necesidad.
- **Conciso**: tarjetas destiladas → máximo ~25-30 líneas.
- **Seco y directo**: imperativos ("Enumerar", "Extraer"), sin relleno.
- **Español**: idioma del proyecto (salvo comandos/herramientas).
- **Sin secretos**: nunca escribir credenciales/tokens reales; solo placeholders.

## 5) Contrato de guardrails (heredado de AGENTS.md)

Toda tarjeta debe respetar:

1. Autorización previa escrita antes del primer request activo.
2. Alcance acotado; sin pivot sin aprobación.
3. Sin exploit sin evidencia reproducible.
4. Rate-limit 200 ms por defecto por host.
5. Evidencia redactada (credenciales → últimos 6 chars; PII oculta).

---

## Ejemplo canónico

```markdown
# SKILL-SQLI.md — SQL Injection

## Cuándo usarla
Parámetros/paths en web/API que parecen consultar una BD (IDs, búsquedas, filtros, login).

## Procedimiento resumido
1. Detectar inyección: `'`, `' OR '1'='1`, `-- -`, `#`, `/*`, y variantes URL-encoded.
2. Confirmar tiempo para blind: `SLEEP(5)`, `pg_sleep(5)`, `WAITFOR DELAY '0:0:5'`.
3. Enumerar con `sqlmap` (solo tras confirmar inyección manual):
   `sqlmap -u "<url>" --batch --level 2 --risk 2` (verificar target autorizado).
4. Extraer: `--dbs`, `-D <db> --tables`, `-T <tabla> --dump --threads 4`.
5. Bypass WAF: variantes de codificación, tablas temporales, `UNION` con comentarios.

## Clasificación de hallazgo
- Error en BD visible / respuesta anómala → L3; dump de datos → L4.

## Herramientas Kali
`sqlmap`, `curl`, Burp Suite para repetir/verificar.

## Guardrails
- Sqlmap en modo agresivo puede cargar la BD objetivo: moderar `--threads`.
- Evidencia: request+response original y después del payload.
- Datos extraídos: solo últimos 6 chars en chat; PII a `findings/secrets-vault.md`.
```

---

Si creas tarjetas nuevas con este formato, considera añadirlas al `INDEX.md` del
área correspondiente y registrarlas en `docs/CATALOGO-SKILLS.md`.

---

## 6) Modo lite y modo full

| Modo | Artefacto | Cuándo |
|---|---|---|
| **lite** | Solo la tarjeta `SKILL-<SLUG>.md` | Cobertura amplia y resumida |
| **full** | `skills/CTF/_full/<skill>/` con `SKILL.md`, `references/`, `scripts/`, `assets/` | Técnica que necesita procedimiento largo y código ejecutable |

Reglas:

- El `manifest.json` declara `kind` (`lite`/`full`) y la ruta de cada variante.
- Precedencia al instalar: **full > lite**. Si existe versión completa, se copia
  el árbol; si no, se materializa la tarjeta como `<id>/SKILL.md`.
- Regenerar el manifiesto tras añadir o mover tarjetas:
  `python tools/build_manifest.py --repo .`
- Validar antes de publicar:
  `python scripts/validate_skills.py --repo . --verbose`
- Instalar:
  `python scripts/install_skills.py --repo . --area CTF --dest ~/.agents/skills`