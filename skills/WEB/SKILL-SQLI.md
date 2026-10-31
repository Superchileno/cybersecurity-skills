---
name: web-sqli
description: 'Parámetros/paths en web/API que parecen consultar una BD (IDs, búsquedas, filtros, login). Keywords: sqli, web.'
area: WEB
tags: [sqli, web]
license: Apache-2.0
---

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